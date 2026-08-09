#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# Instalador do Bíblia Sagrada
# https://github.com/elizeubarbosaabreu/biblia-leitor

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$HOME/.local/share/geradores_de_videos"
BIN_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.local/share/icons"
APP_DIR="$HOME/.local/share/applications"
APP_ID="com.github.elizeubarbosaabreu.BibliaSacra"

echo "=== Bíblia Sagrada - Instalador ==="

# 1. Criar diretórios
echo "Criando diretórios..."
mkdir -p "$BIN_DIR" "$ICON_DIR" "$APP_DIR"

# 2. Criar a venv se não existir
echo "Verificando dependências..."
if [ ! -x "$VENV_DIR/bin/python3" ]; then
    echo "Criando venv em $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Instalar PyQt5 na venv se necessário
if ! "$VENV_DIR/bin/python3" -c "import PyQt5" 2>/dev/null; then
    echo "Instalando PyQt5 na venv..."
    "$VENV_DIR/bin/pip" install --timeout 120 --retries 5 PyQt5
fi

# 4. Remover velho biblia.py do bin (se existir)
rm -f "$BIN_DIR/biblia.py"

# 5. Copiar biblia.py -> ~/.local/bin/biblia (sem extensão)
echo "Instalando executável..."
cp "$SCRIPT_DIR/biblia.py" "$BIN_DIR/biblia"

# 6. Shebang para a venv
sed -i "1s|.*|#!$VENV_DIR/bin/python3|" "$BIN_DIR/biblia"

# 7. Permissão de execução
chmod +x "$BIN_DIR/biblia"

# 8. Copiar ícone
echo "Copiando ícone..."
cp "$SCRIPT_DIR/biblia.png" "$ICON_DIR/biblia.png"

# 9. Criar .desktop
echo "Criando atalho..."
cat > "$APP_DIR/$APP_ID.desktop" << EOF
[Desktop Entry]
Name=Bíblia Sagrada
Comment=Leitor de Bíblia com interface de livro
Exec=$BIN_DIR/biblia
Icon=$ICON_DIR/biblia.png
Terminal=false
Type=Application
Categories=Education;
StartupNotify=true
Keywords=biblia;bible;leitor;reader;
EOF

# 10. Atualizar banco de dados de desktop
command -v update-desktop-database &>/dev/null && update-desktop-database "$APP_DIR"

# 11. Garantir PATH no .bashrc
if ! grep -q '\.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo "Adicionando ~/.local/bin ao PATH no .bashrc..."
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> "$HOME/.bashrc"
    echo "PATH atualizado. Execute: source ~/.bashrc"
fi

echo ""
echo "=== Instalação concluída ==="
echo "  Executável: $BIN_DIR/biblia"
echo "  Ícone:      $ICON_DIR/biblia.png"
echo "  Atalho:     $APP_DIR/$APP_ID.desktop"
echo ""
echo "Execute: biblia"
