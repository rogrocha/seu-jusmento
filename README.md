# 📚 Seu Jusmento

Pipeline de análise jurídica automatizada com NLP e IA.

---

## 🧠 Visão Geral

O projeto `seu-jusmento` tem como objetivo simplificar e analisar automaticamente documentos jurídicos, realizando as seguintes etapas:

1. 📥 Extração de texto de PDFs
2. 🧹 Limpeza e normalização textual
3. 📖 Tradução de jargões jurídicos para linguagem simples
4. 🧾 Geração de resumo automático
5. 🚨 Detecção de falácias argumentativas comuns

---

## 🗂️ Estrutura do Projeto

```bash
seu-jusmento/
├── data/                  # Armazenamento de PDFs e arquivos de entrada
├── notebooks/             # Análises e testes interativos
├── src/                   # Módulos Python organizados
│   ├── cleaning.py        # Função de limpeza de texto
│   ├── fallacies.py       # Detecção de falácias
│   ├── jargon.py          # Tradução de jargões jurídicos
│   ├── ocr.py             # Extração de texto via OCR (PDFs)
│   ├── pipeline.py        # Pipeline completo (executável)
│   └── summarizer.py      # Resumo automático com NLTK ou spaCy
├── tests/                 # Diretório para testes automatizados
├── venv/                  # Ambiente virtual Python
├── .gitignore             # Arquivos a serem ignorados pelo Git
├── requirements.txt       # Dependências do projeto
├── README.md              # Você está aqui 😄
└── pipeline_juridico.py   # (opcional, versão antiga do pipeline)
