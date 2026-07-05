# Bíblia Sagrada - Leitor

Um leitor de Bíblia elegante com interface de livro, texto grande e sistema de marcações.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange?logo=linux&logoColor=white)

---

## Funcionalidades

- **Interface estilo livro** com visual de páginas
- **Texto grande e legível** com fontes Serif de alta qualidade
- **Marcações coloridas** em versículos (amarelo, verde, azul, rosa, laranja)
- **Navegação intuitiva** por livros, capítulos e versículos
- **Suporte a múltiplas versões** bíblicas
- **Salva suas marcações** automaticamente
- **Tamanho de fonte ajustável** (12pt a 36pt)

---

## Versões Suportadas

O aplicativo lê automaticamente as versões instaladas pelo **Bible GUI** (net.lugsole.bible_gui):

| Versão | Formato | Descrição |
|--------|---------|-----------|
| CNBB | SQLite3 | Bíblia CNBB (Nova Capa), 2002 |
| JFA+ | SQLite3 | João Ferreira de Almeida com Strong |
| NTLH | SQLite3 | Nova Tradução na Linguagem de Hoje |
| PorAR | SPB | Bíblia Almeida Recebida |
| PorCapNT | SPB | Bíblia dos Capuchinhos (NT) |
| PorLivre | SPB | Bíblia Livre |
| Portuguese_AlmeidaAtualizada | SPB | Almeida Atualizada |
| Portuguese_AlmeidaCorrigida | SPB | Almeida Corrigida |

---

## Pré-requisitos

- **Python 3.8** ou superior
- **PyQt5** (interface gráfica)
- **Bible GUI** instalado via Flatpak (para as versões bíblicas)

### Instalar dependências

```bash
# Ubuntu/Debian
sudo apt install python3-pyqt5

# Fedora
sudo dnf install python3-qt5

# Arch Linux
sudo pacman -S python-pyqt5
```

---

## Instalação

### Método 1: Instalação rápida (recomendado)

Copie e cole o comando abaixo no seu terminal:

```bash
mkdir -p ~/.local/bin && \
curl -sL https://raw.githubusercontent.com/elizeubarbosaabreu/biblia-leitor/main/biblia -o ~/.local/bin/biblia && \
chmod +x ~/.local/bin/biblia && \
echo "Instalado com sucesso! Execute: biblia"
```

### Método 2: Clonar o repositório

```bash
git clone https://github.com/elizeubarbosaabreu/biblia-leitor.git
cd biblia-leitor
chmod +x biblia
cp biblia ~/.local/bin/
```

### Método 3: Instalar manualmente

1. Baixe o arquivo `biblia`
2. Torne-o executável: `chmod +x biblia`
3. Copie para `~/.local/bin/`: `cp biblia ~/.local/bin/`

---

## Executar

```bash
biblia
```

Ou crie um atalho no menu do sistema criando o arquivo `~/.local/share/applications/biblia.desktop`:

```ini
[Desktop Entry]
Name=Bíblia Sagrada
Comment=Leitor de Bíblia com interface de livro
Exec=biblia
Icon=accessories-dictionary
Terminal=false
Type=Application
Categories=Utility;Education;
Keywords=biblia;bible;leitor;reader;
```

---

## Uso

### Navegação

1. **Selecione a versão** no dropdown "Versão"
2. **Escolha o livro** no dropdown "Livro"
3. **Navegue pelos capítulos** usando os botões ou o seletor numérico
4. **Navegue pelos versículos** da mesma forma

### Marcação de textos

1. **Selecione o versículo** que deseja marcar
2. **Clique numa cor** na barra de ferramentas para aplicar a marcação
3. **Clique em "Limpar"** para remover a marcação do versículo atual

### Copiar versículo

1. **Navegue até o versículo** desejado
2. **Clique em "📋 Copiar Versículo"**
3. O texto será copiado com a referência (ex: "Gênesis 1:1 - No princípio...")
4. **Cole em qualquer lugar** com `Ctrl+V`

### Atalhos de teclado

| Tecla | Ação |
|-------|------|
| `←` | Capítulo/vérsulo anterior |
| `→` | Próximo capítulo/vérsulo |
| `+` | Aumentar fonte |
| `-` | Diminuir fonte |

---

## Localização dos dados

- **Versões bíblicas**: `~/.var/app/net.lugsole.bible_gui/data/net.lugsole.bible_gui/translations/`
- **Marcações salvas**: `~/.local/share/biblia_highlights.json`

---

## Estrutura do projeto

```
biblia-leitor/
├── biblia              # Aplicativo principal (executável Python)
├── README.md           # Este arquivo
├── LICENSE             # Licença MIT
└── screenshots/        # Capturas de tela
```

---

## Solução de problemas

### "Não encontra as versões bíblicas"

Verifique se o Bible GUI está instalado:
```bash
flatpak list | grep bible
```

Se não estiver, instale:
```bash
flatpak install flathub net.lugsole.bible_gui
```

### "Erro: PyQt5 não encontrado"

```bash
pip3 install PyQt5
# ou
sudo apt install python3-pyqt5
```

### "Permissão negada ao executar"

```bash
chmod +x ~/.local/bin/biblia
```

### "Comando biblia não encontrado"

Verifique se `~/.local/bin` está no PATH:
```bash
echo $PATH | grep -q "$HOME/.local/bin" && echo "OK" || echo "Adicione ao ~/.bashrc: export PATH=\"\$HOME/.local/bin:\$PATH\""
```

---

## Contribuindo

Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b nova-feature`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin nova-feature`)
5. Abra um Pull Request

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Créditos

- Desenvolvido com Python e PyQt5
- Compatível com as versões do [Bible GUI](https://flathub.org/apps/net.lugsole.bible_gui)

---

<p align="center">
  <i>"Lâmpada para os meus pés é tua palavra, e luz para o meu caminho."</i><br>
  <b>Salmos 119:105</b>
</p>
