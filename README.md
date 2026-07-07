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

## Instalação

### Opção 1: Flatpak (Recomendado no Linux)

```bash
# Clonar o repositório
git clone https://github.com/elizeubarbosaabreu/biblia-leitor.git
cd biblia-leitor

# Construir e instalar
./build-flatpak.sh

# Executar
flatpak run com.github.elizeubarbosaabreu.BibliaSacra
```

### Opção 2: Executar via Python

```bash
# Clonar o repositório
git clone https://github.com/elizeubarbosaabreu/biblia-leitor.git
cd biblia-leitor

# Instalar dependências
pip install -r requirements.txt

# Executar
python biblia.py
```

### Dependências

- Python 3.8+
- PyQt5

---

## Como Baixar Versões Bíblicas

O aplicativo não vem com versões bíblicas. Você precisa baixar separadamente.

### Repositório Oficial (Recomendado)

Acesse: https://github.com/elizeubarbosaabreu/biblias

Lá você encontra versões em formato `.sqlite` prontas para importar:

| Versão | Descrição |
|--------|-----------|
| **ARA** | Almeida Revisada Atualizada |
| **ACF** | Almeida Corrigida Fiel |
| **ARC** | Almeida Revisada Corrigida |
| **AS21** | Atualizada Segundo a 21ª Edição |
| **JFAA** | João Ferreira de Almeida Atualizada |
| **KJA** | King James Atualizada |
| **KJF** | King James Fiel |
| **NAA** | Nova Almeida Atualizada |
| **NBV** | Nova Bíblia Viva |
| **NTLH** | Nova Tradução na Linguagem de Hoje |
| **NVI** | Nova Versão Internacional |
| **NVT** | Nova Versão Traduzida |
| **TB** | Tradução de Brasília |

### Outras Fontes

- [Bible SuperSearch](https://biblesupersearch.com/download) - Escolha formato SQLite3
- [The SWORD Project](https://www.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles) - Formato .spb

### Importar no Aplicativo

1. Abra o aplicativo Bíblia Sagrada
2. Vá no menu **Arquivo > Importar Versão** (ou pressione `Ctrl+I`)
3. Navegue até o arquivo baixado (`.sqlite`, `.SQLite3` ou `.spb`)
4. Selecione o arquivo e clique em "Abrir"
5. A versão será importada automaticamente

---

## Menu e Atalhos

### Menu Arquivo
| Item | Atalho | Descrição |
|------|--------|-----------|
| Importar Versão | `Ctrl+I` | Importa um arquivo .sqlite, .SQLite3 ou .spb |
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
3. Baixe versões em https://github.com/elizeubarbosaabreu/biblias

### "Erro: PyQt5 não encontrado"

```bash
pip install PyQt5
# ou
sudo apt install python3-pyqt5
```

### "Permissão negada ao executar"

```bash
chmod +x biblia.py
```

### "Arquivo não importa"

- Verifique se o arquivo é `.sqlite`, `.SQLite3` ou `.spb`
- Arquivos `.zip` precisam ser extraídos primeiro

---

## Estrutura do projeto

```
biblia-leitor/
├── biblia.py           # Aplicativo principal
├── biblia.png          # Ícone do aplicativo
├── requirements.txt    # Dependências Python
├── README.md           # Este arquivo
└── LICENSE             # Licença MIT
```

---

## Contribuindo

Contribuições são bem-vindas. Siga estes passos:

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
- **Versões bíblicas:** https://github.com/elizeubarbosaabreu/biblias

---

<p align="center">
  <i>"Lâmpada para os meus pés é tua palavra, e luz para o meu caminho."</i><br>
  <b>Salmos 119:105</b>
</p>
