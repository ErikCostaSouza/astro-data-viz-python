astro-data-viz-python/
│
├── 📁 src/                          # Core do projeto (947 linhas)
│   ├── __init__.py                  # Package initialization
│   ├── fits_reader.py               # Leitura de arquivos FITS (142 linhas)
│   ├── image_processor.py           # Processamento de imagens (245 linhas)
│   ├── rgb_converter.py             # Conversão para RGB (230 linhas)
│   ├── pipeline.py                  # Orquestração (170 linhas)
│   └── synthetic_fits_generator.py  # Geração de dados de teste (160 linhas)
│
├── 📁 notebooks/                    # Demonstrações interativas
│   └── astro_data_viz_demo.ipynb    # 12 seções de demonstração
│
├── 📁 examples/                     # Exemplos progressivos
│   ├── example1_basic.py            # Uso básico
│   ├── example2_colorization.py     # 5 métodos de colorização
│   └── example3_advanced.py         # 10 técnicas avançadas
│
├── 📁 tests/                        # Suite de testes (27 testes)
│   ├── test_fits_reader.py          # 6 testes
│   ├── test_image_processor.py      # 11 testes
│   └── test_rgb_converter.py        # 10 testes
│
├── 📁 data/                         # Dados (gitignore)
│   ├── raw/                         # Arquivos FITS originais
│   └── processed/                   # Imagens PNG processadas
│
├── 📄 Documentation
│   ├── README.md                    # Visão geral
│   ├── README_PROJETO.md            # Documentação detalhada (400+ linhas)
│   ├── API_REFERENCE.md             # Referência de APIs
│   ├── PROJECT_OVERVIEW.md          # Visão técnica do projeto
│   ├── PROJECT_SUMMARY.py           # Script de resumo
│   └── PROJETO_COMPLETO.md          # Documentação completa
│
├── 🔧 Configuração
│   ├── requirements.txt             # Dependências Python
│   ├── setup.py                     # Setup do package
│   ├── setup.bat                    # Setup automatizado (Windows)
│   ├── QUICKSTART.py                # Guia rápido
│   └── .gitignore                   # Git ignore
│
└── 🔐 Controle de versão
    └── .git/                        # Repositório Git
    