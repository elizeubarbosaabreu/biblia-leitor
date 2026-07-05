#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bíblia - Leitor de Bíblia com interface de livro
Suporta versões SQLite3 e SPB

Desenvolvido por: Elizeu Barbosa
Site: https://elizeubarbosa.com.br/
Blog: https://sofagospel.blogspot.com/
"""

import sys
import os
import json
import re
import sqlite3
import shutil
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QScrollArea, QTextEdit,
    QMessageBox, QSplitter, QFrame, QFontComboBox, QSpinBox,
    QFileDialog, QAction, QMenuBar, QMenu, QToolBar, QStatusBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QTextCursor, QIcon

# Caminhos cross-platform
if sys.platform == 'win32':
    BIBLE_DATA_DIR = Path(os.environ.get('APPDATA', Path.home())) / 'xiphos' / 'translations'
    HIGHLIGHTS_FILE = Path(os.environ.get('APPDATA', Path.home())) / 'xiphos' / 'highlights.json'
elif sys.platform == 'darwin':
    BIBLE_DATA_DIR = Path.home() / 'Library' / 'Application Support' / 'xiphos' / 'translations'
    HIGHLIGHTS_FILE = Path.home() / 'Library' / 'Application Support' / 'xiphos' / 'highlights.json'
else:
    BIBLE_DATA_DIR = Path.home() / '.local' / 'share' / 'xiphos' / 'translations'
    HIGHLIGHTS_FILE = Path.home() / '.local' / 'share' / 'xiphos' / 'highlights.json'

# Nomes dos livros em português
BOOK_NAMES_PT = {
    1: "Gênesis", 2: "Êxodo", 3: "Levítico", 4: "Números", 5: "Deuteronômio",
    6: "Josué", 7: "Juízes", 8: "Rute", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Reis", 12: "2 Reis", 13: "1 Crônicas", 14: "2 Crônicas", 15: "Esdras",
    16: "Neemias", 17: "Ester", 18: "Jó", 19: "Salmos", 20: "Provérbios",
    21: "Eclesiastes", 22: "Cântico dos Cânticos", 23: "Isaías", 24: "Jeremias",
    25: "Lamentações", 26: "Ezequiel", 27: "Daniel", 28: "Oséias", 29: "Joel",
    30: "Amós", 31: "Obadias", 32: "Jonas", 33: "Miquéias", 34: "Naum",
    35: "Habacuque", 36: "Sofonias", 37: "Ageu", 38: "Zacarias", 39: "Malaquias",
    40: "Mateus", 41: "Marcos", 42: "Lucas", 43: "João", 44: "Atos",
    45: "Romanos", 46: "1 Coríntios", 47: "2 Coríntios", 48: "Gálatas",
    49: "Efésios", 50: "Filipenses", 51: "Colossenses", 52: "1 Tessalonicenses",
    53: "2 Tessalonicenses", 54: "1 Timóteo", 55: "2 Timóteo", 56: "Tito",
    57: "Filemom", 58: "Hebreus", 59: "Tiago", 60: "1 Pedro", 61: "2 Pedro",
    62: "1 João", 63: "2 João", 64: "3 João", 65: "Judas", 66: "Apocalipse"
}

# Abreviações dos livros
BOOK_ABBR_PT = {
    1: "Gn", 2: "Ex", 3: "Lv", 4: "Nm", 5: "Dt",
    6: "Js", 7: "Jz", 8: "Rt", 9: "1Sm", 10: "2Sm",
    11: "1Rs", 12: "2Rs", 13: "1Cr", 14: "2Cr", 15: "Ed",
    16: "Ne", 17: "Et", 18: "Jó", 19: "Sl", 20: "Pv",
    21: "Ec", 22: "Ct", 23: "Is", 24: "Jr", 25: "Lm",
    26: "Ez", 27: "Dn", 28: "Os", 29: "Jl", 30: "Am",
    31: "Ob", 32: "Jn", 33: "Mq", 34: "Na", 35: "Hc",
    36: "Sf", 37: "Ag", 38: "Zc", 39: "Ml", 40: "Mt",
    41: "Mc", 42: "Lc", 43: "Jo", 44: "At", 45: "Rm",
    46: "1Co", 47: "2Co", 48: "Gl", 49: "Ef", 50: "Fp",
    51: "Cl", 52: "1Ts", 53: "2Ts", 54: "1Tm", 55: "2Tm",
    56: "Tt", 57: "Fm", 58: "Hb", 59: "Tg", 60: "1Pe",
    61: "2Pe", 62: "1Jo", 63: "2Jo", 64: "3Jo", 65: "Jd", 66: "Ap"
}


class BibleLoader:
    """Carrega versões bíblicas dos formatos SQLite3 e SPB"""

    def __init__(self):
        self.versions = {}
        self._load_versions()

    def _load_versions(self):
        if not BIBLE_DATA_DIR.exists():
            BIBLE_DATA_DIR.mkdir(parents=True, exist_ok=True)
            return

        for file_path in BIBLE_DATA_DIR.iterdir():
            if file_path.suffix == '.SQLite3':
                name = file_path.stem
                self.versions[name] = {'type': 'sqlite', 'path': file_path}
            elif file_path.suffix == '.spb':
                name = file_path.stem
                self.versions[name] = {'type': 'spb', 'path': file_path}

    def reload_versions(self):
        self.versions.clear()
        self._load_versions()

    def import_version(self, source_path):
        source = Path(source_path)
        if not source.exists():
            return False, "Arquivo não encontrado"

        if source.suffix not in ('.SQLite3', '.spb', '.sqlite', '.db'):
            return False, f"Formato não suportado: {source.suffix}"

        BIBLE_DATA_DIR.mkdir(parents=True, exist_ok=True)

        if source.suffix == '.sqlite' or source.suffix == '.db':
            dest_name = source.stem + '.SQLite3'
        else:
            dest_name = source.name

        dest_path = BIBLE_DATA_DIR / dest_name

        if dest_path.exists():
            return False, f"Versão '{dest_name}' já existe"

        shutil.copy2(source, dest_path)
        self.reload_versions()
        return True, f"Importada: {dest_name}"

    def delete_version(self, version_name):
        if version_name not in self.versions:
            return False, "Versão não encontrada"

        version_path = self.versions[version_name]['path']

        reply = QMessageBox.question(
            None,
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir a versão '{version_name}'?\n\nArquivo: {version_path}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                version_path.unlink()
                self.reload_versions()
                return True, f"Versão '{version_name}' excluída"
            except Exception as e:
                return False, f"Erro ao excluir: {e}"
        else:
            return False, "Exclusão cancelada"

    def get_version_names(self):
        return sorted(self.versions.keys())

    def load_version(self, version_name):
        if version_name not in self.versions:
            return None

        version_info = self.versions[version_name]

        if version_info['type'] == 'sqlite':
            return self._load_sqlite(version_info['path'])
        else:
            return self._load_spb(version_info['path'])

    def _load_sqlite(self, path):
        conn = sqlite3.connect(str(path))
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM info")
        info = dict(cursor.fetchall())

        cursor.execute("SELECT * FROM books")
        books_raw = cursor.fetchall()

        books = {}
        for book_id, abbr, full_name, color in books_raw:
            book_num = book_id // 10
            books[book_num] = {
                'id': book_id,
                'abbr': abbr,
                'name': full_name if full_name else BOOK_NAMES_PT.get(book_num, f'Livro {book_num}'),
                'color': color
            }

        cursor.execute("SELECT * FROM verses")
        verses_raw = cursor.fetchall()

        verses = {}
        for book_id, chapter, verse, text in verses_raw:
            book_num = book_id // 10
            key = (book_num, chapter)
            if key not in verses:
                verses[key] = {}
            verses[key][verse] = text

        conn.close()

        return {
            'name': info.get('description', 'Desconhecida'),
            'books': books,
            'verses': verses
        }

    def _load_spb(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        title = "Desconhecida"
        for line in lines[:10]:
            if line.startswith('##Title:'):
                title = line.split('\t')[1].strip() if '\t' in line else line[8:].strip()
                break

        books = {}
        verse_start = 0
        for i, line in enumerate(lines):
            if line.strip() == '-----':
                verse_start = i + 1
                break
            if line.startswith('##') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                try:
                    book_num = int(parts[0])
                    book_name = parts[1]
                    num_chapters = int(parts[2])
                    books[book_num] = {
                        'name': BOOK_NAMES_PT.get(book_num, book_name),
                        'chapters': num_chapters
                    }
                except (ValueError, IndexError):
                    continue

        verses = {}
        for line in lines[verse_start:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 5:
                try:
                    book_num = int(parts[1])
                    chapter = int(parts[2])
                    verse = int(parts[3])
                    text = parts[4]
                    key = (book_num, chapter)
                    if key not in verses:
                        verses[key] = {}
                    verses[key][verse] = text
                except (ValueError, IndexError):
                    continue

        return {
            'name': title,
            'books': books,
            'verses': verses
        }


class HighlightManager:
    """Gerencia marcações/highlights do usuário"""

    def __init__(self):
        self.highlights = {}
        self._load()

    def _load(self):
        if HIGHLIGHTS_FILE.exists():
            try:
                with open(HIGHLIGHTS_FILE, 'r', encoding='utf-8') as f:
                    self.highlights = json.load(f)
            except:
                self.highlights = {}

    def _save(self):
        HIGHLIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HIGHLIGHTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.highlights, f, ensure_ascii=False, indent=2)

    def get_highlights(self, version, book, chapter):
        key = f"{version}:{book}:{chapter}"
        return self.highlights.get(key, [])

    def add_highlight(self, version, book, chapter, verse, color):
        key = f"{version}:{book}:{chapter}"
        if key not in self.highlights:
            self.highlights[key] = []

        self.highlights[key] = [h for h in self.highlights[key] if h['verse'] != verse]

        self.highlights[key].append({
            'verse': verse,
            'color': color
        })

        self._save()

    def remove_highlight(self, version, book, chapter, verse):
        key = f"{version}:{book}:{chapter}"
        if key in self.highlights:
            self.highlights[key] = [h for h in self.highlights[key] if h['verse'] != verse]
            if not self.highlights[key]:
                del self.highlights[key]
            self._save()


class BibleReader(QMainWindow):
    """Janela principal do leitor de Bíblia"""

    HIGHLIGHT_COLORS = [
        ("Amarelo", "#FFFF00"),
        ("Verde", "#90EE90"),
        ("Azul", "#ADD8E6"),
        ("Rosa", "#FFB6C1"),
        ("Laranja", "#FFDAB9")
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bíblia Sagrada")
        self.setMinimumSize(900, 700)

        # Ícone
        icon_path = Path.home() / '.local' / 'share' / 'biblia.png'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.loader = BibleLoader()
        self.highlight_manager = HighlightManager()

        self.current_version = None
        self.current_book = None
        self.current_chapter = 1
        self.current_verse = 1
        self.font_size = 18

        self._setup_ui()
        self._load_versions()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Menu bar
        self._create_menu_bar()

        # Barra superior
        top_bar = QHBoxLayout()

        # Versão
        top_bar.addWidget(QLabel("Versão:"))
        self.version_combo = QComboBox()
        self.version_combo.setMinimumWidth(200)
        self.version_combo.currentTextChanged.connect(self._on_version_changed)
        top_bar.addWidget(self.version_combo)

        # Livro
        top_bar.addWidget(QLabel("Livro:"))
        self.book_combo = QComboBox()
        self.book_combo.setMinimumWidth(180)
        self.book_combo.currentIndexChanged.connect(self._on_book_changed)
        top_bar.addWidget(self.book_combo)

        # Capítulo
        top_bar.addWidget(QLabel("Cap:"))
        self.chapter_spin = QSpinBox()
        self.chapter_spin.setMinimum(1)
        self.chapter_spin.setMaximum(150)
        self.chapter_spin.valueChanged.connect(self._on_chapter_changed)
        top_bar.addWidget(self.chapter_spin)

        # Versículo
        top_bar.addWidget(QLabel("Verso:"))
        self.verse_spin = QSpinBox()
        self.verse_spin.setMinimum(1)
        self.verse_spin.setMaximum(200)
        self.verse_spin.valueChanged.connect(self._on_verse_changed)
        top_bar.addWidget(self.verse_spin)

        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Barra de ferramentas
        toolbar = QHBoxLayout()

        # Tamanho da fonte
        toolbar.addWidget(QLabel("Tamanho:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(12)
        self.font_size_spin.setMaximum(36)
        self.font_size_spin.setValue(self.font_size)
        self.font_size_spin.valueChanged.connect(self._on_font_size_changed)
        toolbar.addWidget(self.font_size_spin)

        toolbar.addStretch()

        # Botões de highlight
        toolbar.addWidget(QLabel("Marcações:"))
        for color_name, color_hex in self.HIGHLIGHT_COLORS:
            btn = QPushButton(f"● {color_name}")
            btn.setStyleSheet(f"background-color: {color_hex}; color: black; padding: 5px;")
            btn.clicked.connect(lambda checked, c=color_hex: self._apply_highlight(c))
            toolbar.addWidget(btn)

        # Botão limpar
        clear_btn = QPushButton("✕ Limpar")
        clear_btn.setStyleSheet("background-color: #FF6666; color: white; padding: 5px;")
        clear_btn.clicked.connect(self._clear_highlight)
        toolbar.addWidget(clear_btn)

        main_layout.addLayout(toolbar)

        # Área de leitura estilo livro
        reader_frame = QFrame()
        reader_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 10px;
            }
        """)
        reader_layout = QVBoxLayout(reader_frame)
        reader_layout.setContentsMargins(30, 20, 30, 20)

        # Título do capítulo
        self.chapter_title = QLabel()
        self.chapter_title.setAlignment(Qt.AlignCenter)
        self.chapter_title.setFont(QFont("Serif", 20, QFont.Bold))
        self.chapter_title.setStyleSheet("color: #8B4513; margin-bottom: 10px;")
        reader_layout.addWidget(self.chapter_title)

        # Texto bíblico
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Serif", self.font_size))
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: #FFF8DC;
                color: #333333;
                border: none;
                padding: 10px;
                line-height: 1.6;
            }
        """)
        reader_layout.addWidget(self.text_display)

        main_layout.addWidget(reader_frame)

        # Barra inferior com navegação
        bottom_bar = QHBoxLayout()

        prev_chapter_btn = QPushButton("◄ Capítulo Anterior")
        prev_chapter_btn.clicked.connect(self._prev_chapter)
        bottom_bar.addWidget(prev_chapter_btn)

        prev_verse_btn = QPushButton("◄ Verso Anterior")
        prev_verse_btn.clicked.connect(self._prev_verse)
        bottom_bar.addWidget(prev_verse_btn)

        bottom_bar.addStretch()

        # Indicador de posição
        self.position_label = QLabel()
        self.position_label.setAlignment(Qt.AlignCenter)
        bottom_bar.addWidget(self.position_label)

        bottom_bar.addStretch()

        next_verse_btn = QPushButton("Próximo Verso ►")
        next_verse_btn.clicked.connect(self._next_verse)
        bottom_bar.addWidget(next_verse_btn)

        next_chapter_btn = QPushButton("Próximo Capítulo ►")
        next_chapter_btn.clicked.connect(self._next_chapter)
        bottom_bar.addWidget(next_chapter_btn)

        main_layout.addLayout(bottom_bar)

        # Status bar
        self.statusBar().showMessage("Pronto")

    def _create_menu_bar(self):
        menubar = self.menuBar()

        # Menu Arquivo
        file_menu = menubar.addMenu("&Arquivo")

        # Importar versão
        import_action = QAction("Importar Versao...", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self._import_version)
        file_menu.addAction(import_action)

        # Excluir versão
        delete_action = QAction("Excluir Versao...", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self._delete_version)
        file_menu.addAction(delete_action)

        file_menu.addSeparator()

        # Sair
        exit_action = QAction("Sair", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Editar
        edit_menu = menubar.addMenu("&Editar")

        # Copiar seleção
        copy_selection_action = QAction("Copiar Selecao", self)
        copy_selection_action.setShortcut("Ctrl+C")
        copy_selection_action.triggered.connect(self._copy_selection)
        edit_menu.addAction(copy_selection_action)

        # Copiar versículo
        copy_verse_action = QAction("Copiar Versiculo (citacao)", self)
        copy_verse_action.setShortcut("Ctrl+Shift+C")
        copy_verse_action.triggered.connect(self._copy_verse_citation)
        edit_menu.addAction(copy_verse_action)

        # Copiar capítulo
        copy_chapter_action = QAction("Copiar Capitulo", self)
        copy_chapter_action.setShortcut("Ctrl+Shift+V")
        copy_chapter_action.triggered.connect(self._copy_chapter)
        edit_menu.addAction(copy_chapter_action)

        # Menu Ajuda
        help_menu = menubar.addMenu("&Ajuda")

        help_action = QAction("Como Baixar Versoes...", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self._show_help)
        help_menu.addAction(help_action)

        help_menu.addSeparator()

        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _load_versions(self):
        names = self.loader.get_version_names()
        self.version_combo.addItems(names)
        if names:
            self.version_combo.setCurrentIndex(0)

    def _import_version(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Bíblia (*.SQLite3 *.spb *.sqlite *.db);;Todos (*)")

        if file_dialog.exec_():
            files = file_dialog.selectedFiles()
            if files:
                success, message = self.loader.import_version(files[0])
                if success:
                    self.version_combo.clear()
                    self._load_versions()
                    self.statusBar().showMessage(message, 3000)
                    QMessageBox.information(self, "Sucesso", message)
                else:
                    QMessageBox.warning(self, "Erro", message)

    def _delete_version(self):
        if not self.current_version:
            QMessageBox.warning(self, "Aviso", "Nenhuma versão selecionada")
            return

        success, message = self.loader.delete_version(self.current_version)
        if success:
            self.version_combo.clear()
            self._load_versions()
            self.statusBar().showMessage(message, 3000)
            QMessageBox.information(self, "Sucesso", message)
        elif "cancelada" not in message:
            QMessageBox.warning(self, "Erro", message)

    def _on_version_changed(self, version_name):
        if not version_name:
            return
        self.current_version = version_name
        self.current_data = self.loader.load_version(version_name)
        if self.current_data:
            self._populate_books()
            self._display_chapter()
            self.statusBar().showMessage(f"Versão: {version_name}", 3000)

    def _populate_books(self):
        self.book_combo.clear()
        if not self.current_data:
            return

        books = self.current_data['books']
        for book_num in sorted(books.keys()):
            name = books[book_num].get('name', BOOK_NAMES_PT.get(book_num, f'Livro {book_num}'))
            self.book_combo.addItem(f"{book_num}. {name}", book_num)

        if self.book_combo.count() > 0:
            self.book_combo.setCurrentIndex(0)

    def _on_book_changed(self, index):
        if index < 0:
            return
        self.current_book = self.book_combo.currentData()
        if self.current_book:
            self._update_chapter_range()
            self.current_chapter = 1
            self.chapter_spin.setValue(1)
            self._display_chapter()

    def _update_chapter_range(self):
        if not self.current_data or not self.current_book:
            return

        max_chapter = 1
        for (book, chapter) in self.current_data['verses'].keys():
            if book == self.current_book:
                max_chapter = max(max_chapter, chapter)

        self.chapter_spin.setMaximum(max_chapter)

    def _on_chapter_changed(self, chapter):
        if chapter < 1:
            return
        self.current_chapter = chapter
        self._update_verse_range()
        self._display_chapter()

    def _update_verse_range(self):
        if not self.current_data or not self.current_book:
            return

        key = (self.current_book, self.current_chapter)
        if key in self.current_data['verses']:
            max_verse = max(self.current_data['verses'][key].keys())
            self.verse_spin.setMaximum(max_verse)

    def _on_verse_changed(self, verse):
        if verse < 1:
            return
        self.current_verse = verse
        self._scroll_to_verse(verse)

    def _on_font_size_changed(self, size):
        self.font_size = size
        self.text_display.setFont(QFont("Serif", size))

    def _display_chapter(self):
        if not self.current_data or not self.current_book:
            return

        book_name = self.current_data['books'].get(
            self.current_book, {}
        ).get('name', BOOK_NAMES_PT.get(self.current_book, ''))
        self.chapter_title.setText(f"{book_name} {self.current_chapter}")

        self.text_display.clear()
        key = (self.current_book, self.current_chapter)

        if key not in self.current_data['verses']:
            self.text_display.setPlainText("Capítulo não disponível nesta versão.")
            return

        chapter_verses = self.current_data['verses'][key]
        highlights = self.highlight_manager.get_highlights(
            self.current_version, self.current_book, self.current_chapter
        )
        highlight_map = {h['verse']: h['color'] for h in highlights}

        cursor = self.text_display.textCursor()

        for verse_num in sorted(chapter_verses.keys()):
            text = self._clean_text(chapter_verses[verse_num])

            verse_format = QTextCharFormat()
            if verse_num in highlight_map:
                verse_format.setBackground(QColor(highlight_map[verse_num]))

            num_format = QTextCharFormat()
            num_format.setFontWeight(QFont.Bold)
            num_format.setForeground(QColor("#8B4513"))
            cursor.insertText(f" {verse_num} ", num_format)

            cursor.insertText(f"{text}", verse_format)

            cursor.insertBlock()

        self.position_label.setText(
            f"{book_name} {self.current_chapter}:{self.current_verse}"
        )

    def _clean_text(self, text):
        """Remove tags HTML como <pb/> do texto"""
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def _scroll_to_verse(self, verse):
        text = self.text_display.toPlainText()
        book_name = self.current_data['books'].get(
            self.current_book, {}
        ).get('name', BOOK_NAMES_PT.get(self.current_book, ''))
        self.position_label.setText(
            f"{book_name} {self.current_chapter}:{verse}"
        )

    def _apply_highlight(self, color):
        """Aplica marcação ao versículo atual"""
        if not self.current_version or not self.current_book:
            return

        self.highlight_manager.add_highlight(
            self.current_version,
            self.current_book,
            self.current_chapter,
            self.current_verse,
            color
        )
        self._display_chapter()

    def _clear_highlight(self):
        """Remove marcação do versículo atual"""
        if not self.current_version or not self.current_book:
            return

        self.highlight_manager.remove_highlight(
            self.current_version,
            self.current_book,
            self.current_chapter,
            self.current_verse
        )
        self._display_chapter()

    def _get_verse_abbr(self, book_num):
        """Retorna abreviação do livro"""
        return BOOK_ABBR_PT.get(book_num, f"Lv{book_num}")

    def _get_version_short_name(self):
        """Retorna nome curto da versão"""
        version_names = {
            'Portuguese_(Almeida_Corrigida)': 'ACF',
            'Portuguese_AlmeidaAtualizada': 'ARA',
            'PorAR': 'ARA',
            'PorCapNT': 'NVI',
            'PorLivre': 'Livre',
            'NTLH': 'NTLH',
            'CNBB': 'CNBB',
            'JFA+': 'JFA+',
        }
        return version_names.get(self.current_version, self.current_version)

    def _copy_selection(self):
        """Copia o texto selecionado com referência"""
        cursor = self.text_display.textCursor()
        selected_text = cursor.selectedText()

        if selected_text and self.current_data and self.current_book:
            abbr = self._get_verse_abbr(self.current_book)
            version = self._get_version_short_name()
            citation = f"'{selected_text}' ({abbr}. {self.current_chapter}, {version})"
            clipboard = QApplication.clipboard()
            clipboard.setText(citation)
            self.statusBar().showMessage("Selecao copiada com referencia", 3000)
        elif selected_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_text)
            self.statusBar().showMessage("Selecao copiada", 3000)
        else:
            self.statusBar().showMessage("Nenhum texto selecionado", 3000)

    def _copy_verse_citation(self):
        """Copia o versículo no formato de citação"""
        if not self.current_data or not self.current_book:
            return

        key = (self.current_book, self.current_chapter)
        if key not in self.current_data['verses']:
            return

        chapter_verses = self.current_data['verses'][key]
        if self.current_verse not in chapter_verses:
            return

        book_name = self.current_data['books'].get(
            self.current_book, {}
        ).get('name', BOOK_NAMES_PT.get(self.current_book, ''))

        verse_text = self._clean_text(chapter_verses[self.current_verse])
        abbr = self._get_verse_abbr(self.current_book)
        version = self._get_version_short_name()

        # Formato: "'Texto' (Abbr. Cap:V, Versão)"
        citation = f"'{verse_text}' ({abbr}. {self.current_chapter}:{self.current_verse}, {version})"

        clipboard = QApplication.clipboard()
        clipboard.setText(citation)

        reference = f"{book_name} {self.current_chapter}:{self.current_verse}"
        self.statusBar().showMessage(f"Copiado: {reference}", 3000)

    def _copy_chapter(self):
        """Copia todos os versículos do capítulo"""
        if not self.current_data or not self.current_book:
            return

        key = (self.current_book, self.current_chapter)
        if key not in self.current_data['verses']:
            return

        chapter_verses = self.current_data['verses'][key]
        abbr = self._get_verse_abbr(self.current_book)
        version = self._get_version_short_name()

        lines = []

        for verse_num in sorted(chapter_verses.keys()):
            text = self._clean_text(chapter_verses[verse_num])
            citation = f"'{text}' ({abbr}. {self.current_chapter}:{verse_num}, {version})"
            lines.append(citation)

        full_text = "\n".join(lines)

        clipboard = QApplication.clipboard()
        clipboard.setText(full_text)

        self.statusBar().showMessage(f"Capítulo copiado: {abbr}. {self.current_chapter}", 3000)

    def _prev_chapter(self):
        if self.current_chapter > 1:
            self.chapter_spin.setValue(self.current_chapter - 1)

    def _next_chapter(self):
        max_ch = self.chapter_spin.maximum()
        if self.current_chapter < max_ch:
            self.chapter_spin.setValue(self.current_chapter + 1)

    def _prev_verse(self):
        if self.current_verse > 1:
            self.verse_spin.setValue(self.current_verse - 1)
        elif self.current_chapter > 1:
            self.chapter_spin.setValue(self.current_chapter - 1)

    def _next_verse(self):
        max_ver = self.verse_spin.maximum()
        if self.current_verse < max_ver:
            self.verse_spin.setValue(self.current_verse + 1)
        else:
            max_ch = self.chapter_spin.maximum()
            if self.current_chapter < max_ch:
                self.chapter_spin.setValue(self.current_chapter + 1)
                self.verse_spin.setValue(1)

    def _show_help(self):
        """Mostra ajuda sobre como baixar versoes"""
        help_text = """
        <h2>Como Baixar e Instalar Versoes Biblicas</h2>
        
        <h3>Passo 1: Baixar as versoes</h3>
        <p>O aplicativo nao vem com versoes biblicas. Voce precisa baixar separadamente.</p>
        
        <h3>Opcao 1: Bible SuperSearch (Recomendado)</h3>
        <ol>
        <li>Acesse: <a href="https://biblesupersearch.com/download">biblesupersearch.com/download</a></li>
        <li>Clique em "Download" na versao desejada</li>
        <li>Escolha o formato <b>SQLite3</b></li>
        <li>Salve o arquivo no seu computador</li>
        </ol>
        
        <h3>Opcao 2: The SWORD Project</h3>
        <ol>
        <li>Acesse: <a href="https://www.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles">crosswire.org</a></li>
        <li>Procure versoes em portugues</li>
        <li>Baixe o arquivo ZIP</li>
        <li>Extraia o conteudo</li>
        </ol>
        
        <h3>Passo 2: Importar no aplicativo</h3>
        <ol>
        <li>Abra o aplicativo Biblia Sagrada</li>
        <li>Va no menu <b>Arquivo > Importar Versao</b> (ou pressione Ctrl+I)</li>
        <li>Navegue ate o arquivo baixado (.SQLite3 ou .spb)</li>
        <li>Selecione o arquivo e clique em "Abrir"</li>
        <li>A versao sera importada automaticamente</li>
        </ol>
        
        <h3>Passo 3: Selecionar a versao</h3>
        <ol>
        <li>No dropdown "Versao" na barra superior</li>
        <li>Selecione a versao que voce importou</li>
        <li>Pronto! Agora voce pode ler a Biblia</li>
        </ol>
        
        <h3>Versoes Populares</h3>
        <ul>
        <li><b>ARA</b> - Almeida Revisada Atualizada</li>
        <li><b>ACF</b> - Almeida Corrigida Fiel</li>
        <li><b>NVI</b> - Nova Versao Internacional</li>
        <li><b>CNBB</b> - Biblia CNBB</li>
        <li><b>NTLH</b> - Nova Traducao na Linguagem de Hoje</li>
        </ul>
        
        <h3>Formatos Suportados</h3>
        <ul>
        <li><b>.SQLite3</b> - Formato padrao</li>
        <li><b>.spb</b> - Formato The SWORD Project</li>
        </ul>
        
        <p><b>Dica:</b> Arquivos .zip precisam ser extraidos primeiro!</p>
        """
        msg = QMessageBox()
        msg.setWindowTitle("Ajuda - Como Baixar Versoes")
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.setOpenExternalLinks(True)
        msg.exec_()

    def _show_about(self):
        """Mostra janela Sobre"""
        about_text = """
        <h2>Bíblia Sagrada</h2>
        <p><b>Leitor de Bíblia com interface de livro</b></p>
        <p>Versão: 2.0</p>
        <hr>
        <p><b>Desenvolvido por:</b><br>
        Elizeu Barbosa</p>
        <p><b>Site:</b><br>
        <a href="https://elizeubarbosa.com.br/">elizeubarbosa.com.br</a></p>
        <p><b>Blog:</b><br>
        <a href="https://sofagospel.blogspot.com/">sofagospel.blogspot.com</a></p>
        <hr>
        <p><b>Funcionalidades:</b></p>
        <ul>
        <li>Interface estilo livro</li>
        <li>Múltiplas versões bíblicas</li>
        <li>Marcações coloridas</li>
        <li>Citação de versículos</li>
        <li>Suporte a SQLite3 e SPB</li>
        </ul>
        <hr>
        <p><i>"Lâmpada para os meus pés é tua palavra,<br>
        e luz para o meu caminho."</i><br>
        <b>Salmos 119:105</b></p>
        """
        QMessageBox.about(self, "Sobre - Bíblia Sagrada", about_text)


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QMainWindow {
            background-color: #F5F5DC;
        }
        QComboBox, QSpinBox {
            padding: 5px;
            font-size: 14px;
        }
        QPushButton {
            padding: 8px 12px;
            font-size: 12px;
            border: 1px solid #8B4513;
            border-radius: 5px;
            background-color: #DEB887;
        }
        QPushButton:hover {
            background-color: #D2691E;
            color: white;
        }
        QLabel {
            font-size: 14px;
            color: #333;
        }
        QMenuBar {
            background-color: #DEB887;
            color: #333;
        }
        QMenuBar::item:selected {
            background-color: #D2691E;
            color: white;
        }
        QMenu {
            background-color: #FFF8DC;
            border: 1px solid #8B4513;
        }
        QMenu::item:selected {
            background-color: #D2691E;
            color: white;
        }
        QStatusBar {
            background-color: #DEB887;
            color: #333;
        }
    """)

    window = BibleReader()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
