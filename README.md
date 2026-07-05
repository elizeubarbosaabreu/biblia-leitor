# Bíblia Sagrada - Leitor

Um leitor de Bíblia elegante com interface de livro, texto grande e sistema de marcações.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-orange)

---

## Funcionalidades

- **Interface estilo livro** com visual de páginas
- **Texto grande e legível** com fontes Serif de alta qualidade
- **Marcações coloridas** em versículos (amarelo, verde, azul, rosa, laranja)
- **Navegação intuitiva** por livros, capítulos e versículos
- **Suporte a múltiplas versões** bíblicas
- **Salva suas marcações** automaticamente
- **Tamanho de fonte ajustável** (12pt a 36pt)
- **Importar versões** - menu para importar arquivos .SQLite3 e .spb
- **Copiar com citação** - formato: 'Texto' (Abbr. Cap:V, Versão)
- **Cross-platform** - Linux, Windows e macOS

---

## Download

### Linux (AppImage)

```bash
# Baixar o AppImage
wget https://github.com/elizeubarbosaabreu/biblia-leitor/releases/download/v2.0/BibliaSacra-x86_64.AppImage

# Tornar executável
chmod +x BibliaSacra-x86_64.AppImage

# Executar
./BibliaSacra-x86_64.AppImage
```

### Linux (executável standalone)

```bash
# Baixar o executável
wget https://github.com/elizeubarbosaabreu/biblia-leitor/releases/download/v2.0/BibliaSacra

# Tornar executável
chmod +x BibliaSacra

# Executar
./BibliaSacra
```

### Python (qualquer plataforma)

```bash
# Instalar dependências
pip install PyQt5

# Baixar o script
wget https://raw.githubusercontent.com/elizeubarbosaabreu/biblia-leitor/master/biblia

# Tornar executável
chmod +x biblia

# Executar
./biblia
```

---

## Como Baixar e Instalar Versões Bíblicas

### Passo 1: Baixar as versões

O aplicativo não vem com versões bíblicas. Você precisa baixar separadamente.

#### Opção 1: Bible SuperSearch (Recomendado)

1. Acesse: https://biblesupersearch.com/download
2. Clique em "Download" na versão desejada
3. Escolha o formato **SQLite3**
4. Salve o arquivo no seu computador

#### Opção 2: The SWORD Project

1. Acesse: https://www.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles
2. Procure versões em português
3. Baixe o arquivo ZIP
4. Extraia o conteúdo (será um arquivo .txt ou .zip)

#### Opção 3: Xiphos

1. Instale o Xiphos: https://xiphos.org
2. Abra o Xiphos e vá em "File" > "Import"
3. Exporte a versão desejada
4. Salve como arquivo .spb

### Passo 2: Importar no aplicativo

1. Abra o aplicativo Bíblia Sagrada
2. Vá no menu **Arquivo > Importar Versão** (ou pressione `Ctrl+I`)
3. Navegue até o arquivo baixado (`.SQLite3` ou `.spb`)
4. Selecione o arquivo e clique em "Abrir"
5. A versão será importada automaticamente

### Passo 3: Selecionar a versão

1. No dropdown "Versão" na barra superior
2. Selecione a versão que você importou
3. Pronto! Agora você pode ler a Bíblia

---

## Versões Populares em Português

| Versão | Formato | Descrição | Onde baixar |
|--------|---------|-----------|-------------|
| **ARA** | SPB | Almeida Revisada Atualizada | [Bible SuperSearch](https://biblesupersearch.com/download) |
| **ACF** | SPB | Almeida Corrigida Fiel | [Bible SuperSearch](https://biblesupersearch.com/download) |
| **NVI** | SQLite3 | Nova Versão Internacional | [Bible SuperSearch](https://biblesupersearch.com/download) |
| **CNBB** | SQLite3 | Bíblia CNBB (Nova Capa) | [Bible SuperSearch](https://biblesupersearch.com/download) |
| **NTLH** | SQLite3 | Nova Tradução na Linguagem de Hoje | [Bible SuperSearch](https://biblesupersearch.com/download) |
| **KJV** | SPB | King James Version (inglês) | [Bible SuperSearch](https://biblesupersearch.com/download) |

---

## Menu e Atalhos

### Menu Arquivo
| Item | Atalho | Descrição |
|------|--------|-----------|
| Importar Versão | `Ctrl+I` | Importa um arquivo .SQLite3 ou .spb |
| Excluir Versão | `Delete` | Remove a versão selecionada |
| Sair | `Ctrl+Q` | Fecha o aplicativo |

### Menu Editar
| Item | Atalho | Descrição |
|------|--------|-----------|
| Copiar Seleção | `Ctrl+C` | Copia o texto selecionado com referência |
| Copiar Versículo | `Ctrl+Shift+C` | Copia o versículo no formato citação |
| Copiar Capítulo | `Ctrl+Shift+V` | Copia todos os versículos do capítulo |

### Formato de Citação
```
'Texto do versículo' (Abbr. Cap:V, Versão)
```

Exemplo:
```
'Assim resplandeça a vossa luz diante dos homens, para que vejam as vossas boas obras e glorifiquem a vosso Pai, que está nos céus.' (Mt. 5:16, ARA)
```

---

## Localização dos dados

| Sistema | Caminho |
|---------|---------|
| **Linux** | `~/.local/share/xiphos/translations/` |
| **Windows** | `%APPDATA%/xiphos/translations/` |
| **macOS** | `~/Library/Application Support/xiphos/translations/` |

---

## Solução de problemas

### "Não encontra as versões bíblicas"

1. Verifique se você importou alguma versão
2. Vá em **Arquivo > Importar Versão**
3. Selecione um arquivo `.SQLite3` ou `.spb`

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

### "Arquivo não importa"

- Verifique se o arquivo é `.SQLite3` ou `.spb`
- Arquivos `.zip` precisam ser extraídos primeiro
- Arquivos `.bbk` (E-Sword) precisam ser convertidos

---

## Estrutura do projeto

```
biblia-leitor/
├── biblia              # Aplicativo principal (executável Python)
├── biblia.png          # Ícone do aplicativo
├── BibliaSacra         # Executável standalone (Linux)
├── BibliaSacra-x86_64.AppImage  # AppImage (Linux)
├── README.md           # Este arquivo
└── LICENSE             # Licença MIT
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

- **Desenvolvido por:** Elizeu Barbosa
- **Site:** https://elizeubarbosa.com.br/
- **Blog:** https://sofagospel.blogspot.com/
- **Tecnologias:** Python e PyQt5
- **Formatos suportados:** SQLite3 e SPB (The SWORD Project)

---

<p align="center">
  <i>"Lâmpada para os meus pés é tua palavra, e luz para o meu caminho."</i><br>
  <b>Salmos 119:105</b>
</p>
