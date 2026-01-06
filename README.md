# 📁 Separador Automático de PDFs por Data

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OCR](https://img.shields.io/badge/OCR-Tesseract-orange.svg)](https://github.com/tesseract-ocr/tesseract)

## 🎯 Sobre o Projeto

Este projeto nasceu da necessidade de organizar **centenas de certificados digitais** que eu recebia em PDF ao longo de cursos e treinamentos. Antes, eu gastava horas organizando manualmente esses arquivos por data de conclusão, renomeando pastas e movendo arquivos um por um.

**O problema?** Além do tempo perdido, era comum cometer erros ao digitar datas manualmente ou perder arquivos importantes no meio de tantas pastas.

**A solução?** Desenvolvi esta automação em Python que:
- ✅ Lê automaticamente a data de conclusão de cada certificado PDF
- ✅ Cria pastas organizadas por data (formato DD-MM-AAAA)
- ✅ Move os arquivos para as pastas corretas automaticamente
- ✅ Suporta PDFs digitais e escaneados (usando OCR)
- ✅ Processa múltiplos formatos de data em português

### 💡 Impacto

Esta automação me economiza **mais de 3 horas por mês** que antes eram gastas em organização manual, além de eliminar completamente erros humanos na classificação dos documentos.

---

## 🚀 Funcionalidades

### 🔍 Extração Inteligente de Datas
- **PDFs Digitais**: Extração direta de texto usando `pdfplumber` e `PyPDF2`
- **PDFs Escaneados**: OCR automático usando Tesseract com rotação inteligente
- **Datas por Extenso**: Reconhece padrões como "15 de setembro de 2025"
- **Múltiplas Estratégias**: Tenta diferentes métodos até conseguir extrair a data

### 📂 Organização Automática
- Cria pastas no formato `DD-MM-AAAA` (ex: `15-09-2025`)
- Move automaticamente os PDFs para as pastas correspondentes
- PDFs sem data detectável vão para a pasta `SEM_DATA`
- Relatório completo de processamento ao final

### 🔄 Processamento em Lote
- Processa todos os PDFs da pasta `Arquivos/` de uma vez
- Exibe progresso detalhado em tempo real
- Gera estatísticas de sucesso e falhas

---

## 📋 Pré-requisitos

### 1. Python 3.8 ou superior
Verifique se o Python está instalado:
```bash
python --version
```

Se não tiver instalado, baixe em: [python.org](https://www.python.org/downloads/)

### 2. Tesseract OCR (para PDFs escaneados)

#### Windows
1. Baixe o instalador: [Tesseract OCR Windows](https://github.com/UB-Mannheim/tesseract/wiki)
2. Execute o instalador e anote o caminho de instalação (geralmente `C:\Program Files\Tesseract-OCR`)
3. Adicione ao PATH do sistema ou configure no código

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

#### macOS
```bash
brew install tesseract tesseract-lang
```

### 3. Poppler (para conversão de PDF em imagens)

#### Windows
1. Baixe o Poppler para Windows: [Poppler Releases](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extraia para uma pasta (ex: `C:\Program Files\poppler-xx\Library\bin`)
3. Adicione a pasta `bin` ao PATH do sistema

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install poppler-utils
```

#### macOS
```bash
brew install poppler
```

---

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/separador-de-data.git
cd separador-de-data
```

### 2. Crie um ambiente virtual (recomendado)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências Python
```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` não existir, instale manualmente:
```bash
pip install pdfplumber PyPDF2 pdf2image pytesseract Pillow
```

### 4. Configure o Tesseract (se necessário)
Se o Tesseract não estiver no PATH, adicione esta linha no código (linha ~185):
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 📦 Estrutura do Projeto

```
SeparadorDeData/
│
├── separador_por_data.py    # Script principal
├── Arquivos/                 # Pasta onde os PDFs devem ser colocados
│   ├── certificado1.pdf
│   └── certificado2.pdf
│
├── .venv/                    # Ambiente virtual (criado após instalação)
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

---

## 🎮 Como Usar

### Passo 1: Prepare seus PDFs
Coloque todos os certificados/documentos PDF que deseja organizar na pasta `Arquivos/`

### Passo 2: Execute o script
```bash
python separador_por_data.py
```

### Passo 3: Acompanhe o progresso
O script exibirá em tempo real:
- Nome de cada PDF sendo processado
- Se a data foi encontrada e qual é
- Para onde o arquivo foi movido
- Estatísticas finais

### Exemplo de Saída
```
[INICIO] Iniciando separacao de PDFs por data...

[INFO] Encontrados 65 arquivos PDF

[PROCESSANDO] certificado_python.pdf
   [SUCESSO] Data encontrada: 15/09/2025
   [MOVIDO] 15-09-2025/

[PROCESSANDO] certificado_javascript.pdf
      [OCR] Processando com OCR...
   [SUCESSO] Data encontrada: 22/10/2025
   [MOVIDO] 22-10-2025/

============================================================
RESUMO DA OPERACAO
============================================================
[OK] PDFs processados: 65
[OK] PDFs com data encontrada: 62
[ERRO] PDFs sem data: 3
============================================================
```

### Resultado
Após a execução, a pasta `Arquivos/` terá esta estrutura:
```
Arquivos/
├── 15-09-2025/
│   └── certificado_python.pdf
├── 22-10-2025/
│   └── certificado_javascript.pdf
├── 05-11-2025/
│   └── certificado_java.pdf
└── SEM_DATA/
    └── documento_sem_data.pdf
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| **Python 3.8+** | Linguagem principal |
| **pdfplumber** | Extração de texto de PDFs digitais |
| **PyPDF2** | Alternativa para leitura de PDFs |
| **pdf2image** | Conversão de PDF para imagens |
| **pytesseract** | Interface Python para Tesseract OCR |
| **Pillow (PIL)** | Processamento de imagens |
| **Tesseract OCR** | Motor de reconhecimento óptico de caracteres |
| **Poppler** | Renderização de PDFs |

---

## 🧠 Como Funciona

### 1. Detecção de PDFs
O script busca todos os arquivos `.pdf` na pasta `Arquivos/`

### 2. Extração de Texto (Estratégia em Cascata)
```
┌─────────────────┐
│ Tenta pdfplumber│
└────────┬────────┘
         │ Falhou?
         ▼
┌─────────────────┐
│  Tenta PyPDF2   │
└────────┬────────┘
         │ Falhou?
         ▼
┌─────────────────┐
│ OCR + Rotação   │
│   (Tesseract)   │
└─────────────────┘
```

### 3. Extração de Datas
- Usa **expressões regulares** para encontrar padrões de data
- Procura por: `DD de MÊS de AAAA` (ex: "15 de setembro de 2025")
- Converte meses por extenso para números
- Valida datas para evitar falsos positivos

### 4. Organização
- Cria pasta com nome `DD-MM-AAAA`
- Move o PDF para a pasta correspondente
- Se não encontrar data → move para `SEM_DATA/`

---

## 🐛 Solução de Problemas

### ❌ Erro: "Tesseract not found"
**Solução**: 
- Verifique se o Tesseract está instalado
- Adicione ao PATH ou configure manualmente no código

### ❌ Erro: "Unable to get page count. Is poppler installed?"
**Solução**:
- Instale o Poppler conforme instruções acima
- Adicione a pasta `bin` do Poppler ao PATH

### ❌ PDFs não têm a data extraída
**Possíveis causas**:
- PDF está em formato de imagem de baixa qualidade
- Data não está no formato esperado
- Idioma do PDF não é português

**Soluções**:
- Aumente o DPI do OCR (linha ~187: `dpi=300`)
- Verifique se o pacote de idioma português do Tesseract está instalado
- Adapte as expressões regulares para outros formatos de data

---

## 🔮 Melhorias Futuras

- [ ] Interface gráfica (GUI) com Tkinter ou PyQt
- [ ] Suporte para outros formatos de data (DD/MM/AAAA, ISO 8601)
- [ ] Processamento paralelo para grandes volumes
- [ ] Configuração via arquivo `.env` ou `.config`
- [ ] Suporte para outros idiomas além do português
- [ ] Logs em arquivo para auditoria
- [ ] Opção de cópia ao invés de mover arquivos

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

**Luis Felype**

- GitHub: [@DevLust](https://github.com/DevLust)
- LinkedIn: [Luis Felype](https://www.linkedin.com/in/luis-felype-68a9682b8)

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

---

## ⭐ Agradecimentos

Se este projeto foi útil para você, considere dar uma ⭐ no repositório!

---

<div align="center">
  
**Transformando horas de trabalho manual em segundos de automação** 🚀

</div>
