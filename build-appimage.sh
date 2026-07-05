#!/bin/bash
set -e

echo "=== Build BibliaSacra AppImage ==="
echo ""

# Verificar dependências
echo "[1/6] Verificando dependências..."
for cmd in python3 pip3; do
    if ! command -v $cmd &> /dev/null; then
        echo "ERRO: $cmd não encontrado"
        exit 1
    fi
done

# Verificar/instalar ferramentas necessárias
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Instalando PyInstaller..."
    pip3 install pyinstaller
fi

if ! command -v appimagetool &> /dev/null; then
    echo "Baixando appimagetool..."
    ARCH=$(uname -m)
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-${ARCH}.AppImage" -O /tmp/appimagetool
    chmod +x /tmp/appimagetool
    APPIMAGETOOL="/tmp/appimagetool"
else
    APPIMAGETOOL="appimagetool"
fi

# Limpar builds anteriores
echo "[2/6] Limpando builds anteriores..."
rm -rf build/ dist/ AppDir/
mkdir -p AppDir/usr/{bin,share/applications,share/icons/hicolor/256x256/apps}

# Build PyInstaller em modo --onedir (CRÍTICO para AppImage)
echo "[3/6] Build PyInstaller (modo --onedir)..."
pyinstaller \
    --noconfirm \
    --clean \
    --name BibliaSacra \
    --noconsole \
    --onedir \
    --icon biblia.png \
    --add-data "biblia.png:." \
    --hidden-import PyQt5.QtWidgets \
    --hidden-import PyQt5.QtCore \
    --hidden-import PyQt5.QtGui \
    biblia.py

# Estruturar o AppDir
echo "[4/6] Montando AppDir..."
# Copiar binário e dependências
cp -r dist/BibliaSacra/* AppDir/usr/bin/
chmod +x AppDir/usr/bin/BibliaSacra

# Copiar ícone
cp biblia.png AppDir/usr/share/icons/hicolor/256x256/apps/biblia.png
cp biblia.png AppDir/.DirIcon
cp biblia.png AppDir/biblia.png

# Criar desktop file
cat > AppDir/biblia.desktop << 'EOF'
[Desktop Entry]
Name=Bíblia Sagrada
Comment=Leitor de Bíblia com interface de livro
Exec=BibliaSacra
Icon=biblia
Terminal=false
Type=Application
Categories=Utility;Education;
Keywords=biblia;bible;leitor;reader;
EOF

# Criar AppRun correto
cat > AppDir/AppRun << 'APPRUNEOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}

export PATH="${HERE}/usr/bin/:${PATH}"
export XDG_DATA_DIRS="${HERE}/usr/share/:${XDG_DATA_DIRS:-/usr/local/share/:/usr/share/}"

# Definir QT plugin path para o AppImage
if [ -d "${HERE}/usr/bin/PyQt5/Qt5/plugins" ]; then
    export QT_PLUGIN_PATH="${HERE}/usr/bin/PyQt5/Qt5/plugins"
elif [ -d "${HERE}/usr/bin/qt5_plugins" ]; then
    export QT_PLUGIN_PATH="${HERE}/usr/bin/qt5_plugins"
fi

# PyInstaller onedir: executável está direto em usr/bin/
exec "${HERE}/usr/bin/BibliaSacra" "$@"
APPRUNEOF
chmod +x AppDir/AppRun

# Gerar AppImage
echo "[5/6] Gerando AppImage..."
ARCH=$(uname -m)
ARCHIVE_NAME="BibliaSacra-${ARCH}.AppImage"

# Usar APPIMAGETOOL sem update information para builds locais
$APPIMAGETOOL --no-appstream AppDir "$ARCHIVE_NAME" 2>&1 || {
    echo "Tentando com variáveis de ambiente..."
    ARCH=$ARCH UPDATE_INFO= APPIMAGETOOL_DISABLE_UPDATE_INFORMATION=1 \
    $APPIMAGETOOL AppDir "$ARCHIVE_NAME"
}

chmod +x "$ARCHIVE_NAME"

echo "[6/6] Limpeza..."
rm -rf build/

echo ""
echo "=== Build concluído ==="
echo "AppImage gerado: $ARCHIVE_NAME"
echo "Tamanho: $(ls -lh "$ARCHIVE_NAME" | awk '{print $5}')"
echo ""
echo "Para testar:"
echo "  ./$ARCHIVE_NAME"
echo ""
echo "Para distribuir, copie $ARCHIVE_NAME para o diretório desejado."
