#!/bin/bash
set -e

echo "=== Build Flatpak Bíblia Sagrada ==="
echo ""

# Verificar dependências
echo "[1/4] Verificando dependências..."
if ! command -v flatpak &> /dev/null; then
    echo "ERRO: flatpak não encontrado"
    echo "Instale: sudo apt install flatpak"
    exit 1
fi

if ! command -v flatpak-builder &> /dev/null; then
    echo "flatpak-builder não encontrado. Instalando..."
    sudo apt install -y flatpak-builder
fi

# Adicionar repositório Flathub se não existir
echo "[2/4] Verificando repositório Flathub..."
if ! flatpak remote-list | grep -q flathub; then
    echo "Adicionando Flathub..."
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
fi

# Instalar runtime KDE se não existir
echo "[3/4] Verificando runtime KDE..."
if ! flatpak list --runtime | grep -q "org.kde.Platform"; then
    echo "Instalando runtime KDE 5.15-23.08..."
    flatpak install -y flathub org.kde.Platform//5.15-23.08
    flatpak install -y flathub org.kde.Sdk//5.15-23.08
fi

# Build
echo "[4/4] Construindo Flatpak..."
flatpak-builder --force-clean --install-deps-from=flathub builddir com.github.elizeubarbosaabreu.BibliaSacra.json

echo ""
echo "=== Build concluído ==="
echo ""
echo "Para instalar:"
echo "  flatpak-builder --user --install --force-clean builddir com.github.elizeubarbosaabreu.BibliaSacra.json"
echo ""
echo "Para executar:"
echo "  flatpak run com.github.elizeubarbosaabreu.BibliaSacra"
echo ""
echo "Para exportar como bundle (.flatpak):"
echo "  flatpak build-export repo builddir"
echo "  flatpak build-bundle repo BibliaSacra.flatpak com.github.elizeubarbosaabreu.BibliaSacra"
