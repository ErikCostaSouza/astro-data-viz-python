# Astro Data Visualization - Pipeline Python

Projeto completo de visualização de dados astronômicos em Python para transformar arquivos FITS brutos em imagens RGB coloridas, simulando o processamento de imagens de telescópios como Hubble e JWST.

## 📋 Visão Geral

Este projeto implementa um pipeline completo de processamento de dados FITS (Flexible Image Transport System) que:

- ✅ Carrega e analisa arquivos FITS de observatórios espaciais
- ✅ Aplica técnicas avançadas de processamento de imagem
- ✅ Mapeia múltiplas bandas espectrais para cores RGB
- ✅ Gera imagens coloridas de alta qualidade
- ✅ Suporta diferentes paletas e métodos de colorização

## 🏗️ Estrutura do Projeto

```
astro-data-viz-python/
├── src/
│   ├── __init__.py
│   ├── fits_reader.py              # Leitura de arquivos FITS
│   ├── image_processor.py          # Processamento de imagens
│   ├── rgb_converter.py            # Conversão para RGB
│   ├── pipeline.py                 # Pipeline principal
│   └── synthetic_fits_generator.py # Gerador de dados sintéticos
├── examples/
│   ├── example1_basic.py           # Exemplo básico
│   ├── example2_colorization.py    # Métodos de colorização
│   └── example3_advanced.py        # Técnicas avançadas
├── tests/
│   ├── test_fits_reader.py
│   ├── test_image_processor.py
│   └── test_rgb_converter.py
├── data/
│   ├── raw/                        # Arquivos FITS originais
│   └── processed/                  # Imagens RGB geradas
├── notebooks/                      # Jupyter notebooks
├── requirements.txt
└── README.md
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.7+
- pip ou conda

### Instalação de Dependências

```bash
# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Dependências Principais

- **numpy**: Computação numérica
- **scipy**: Processamento científico
- **astropy**: Manipulação de dados astronômicos (FITS)
- **Pillow**: Processamento de imagens
- **matplotlib**: Visualização
- **scikit-image**: Processamento avançado de imagens

## 📖 Como Usar

### Exemplo Básico

```python
from src.pipeline import AstroDataVizPipeline

# Cria pipeline
pipeline = AstroDataVizPipeline("data/processed")

# Processa um arquivo FITS
rgb, output_path = pipeline.process_fits_to_rgb(
    "data/raw/sua_imagem.fits",
    output_name="minha_imagem"
)

print(f"Imagem salva em: {output_path}")
```

### Leitura de FITS

```python
from src.fits_reader import FITSReader

# Carrega e inspeciona arquivo FITS
with FITSReader("arquivo.fits") as reader:
    data = reader.get_primary_data()
    print(reader.get_info())
```

### Processamento de Imagem

```python
from src.image_processor import ImageProcessor

# Aplica pipeline de processamento
processed = ImageProcessor.apply_pipeline(
    raw_data,
    normalize_method="percentile",
    stretch_method="asinh",
    enhance=True,
    smooth_kernel=3
)
```

### Conversão RGB

```python
from src.rgb_converter import RGBConverter

# Combina três canais em RGB
rgb = RGBConverter.combine_channels(red, green, blue)

# Coloriza imagem monocromática
rgb = RGBConverter.colorize_monochrome(data, colormap="hot")
```

## 🔧 Módulos Principais

### fits_reader.py
Leitura e análise de arquivos FITS astronômicos.

**Classes:**
- `FITSReader`: Leitor completo de FITS

**Funções:**
- `load_fits()`: Helper para carregamento rápido
- `load_fits_multi_channel()`: Carrega múltiplos canais

**Recursos:**
- Suporta HDUs primárias e extensões
- Extrai headers FITS
- Análise de metadados

### image_processor.py
Processamento avançado de imagens astronômicas.

**Técnicas Implementadas:**
- Normalização (minmax, percentil, z-score)
- Stretching (asinh, raiz quadrada, logarítmico)
- Realce de contraste
- Suavização e aguçamento
- Remoção de outliers
- Tratamento de valores NaN

### rgb_converter.py
Conversão de dados monocromáticos ou multi-banda para RGB.

**Métodos:**
- Combinação de canais RGB
- Paletas Hubble e cores naturais
- Colorização com colormaps
- Falsa cor infravermelha
- Equalização de canais

### pipeline.py
Orquestração do processamento end-to-end.

**Funcionalidades:**
- Processamento automático FITS → RGB
- Suporte para múltiplos arquivos
- Cache de imagens processadas
- Salvamento em PNG

### synthetic_fits_generator.py
Gerador de dados FITS sintéticos para testes.

**Recursos:**
- Simula diferentes tipos de objetos astronômicos
- Cria arquivos FITS multi-banda
- Fornece dados de teste realistas

## 💡 Exemplos

### Executar Exemplo Básico

```bash
python examples/example1_basic.py
```

Processa arquivos FITS sintéticos e gera imagens RGB.

### Testar Diferentes Colorizações

```bash
python examples/example2_colorization.py
```

Demonstra múltiplos métodos de conversão para RGB.

### Técnicas Avançadas

```bash
python examples/example3_advanced.py
```

Explora diferentes técnicas de processamento e stretching.

## 🧪 Testes

Execute a suite de testes:

```bash
# Todos os testes
python -m pytest tests/

# Teste específico
python -m pytest tests/test_fits_reader.py

# Com verbosidade
python -m pytest -v tests/
```

## 📚 Conceitos Astronômicos Implementados

### Bandas Espectrais
O projeto simula observações em diferentes comprimentos de onda (UV, Azul, Verde, Vermelho, Infravermelho), como feito por telescópios reais.

### Stretching
Técnicas para melhorar a visualização de dados com grande dinâmica:
- **Asinh**: Suaviza variações não-lineares
- **Log**: Comprime dados com grande intervalo dinâmico
- **Sqrt**: Suave e linear

### Paletas de Cor
- **Natural**: Aproxima cores reais (R=Vermelho, G=Verde, B=Azul)
- **Hubble**: Paleta clássica do Hubble (R=IR, G=Vermelho, B=Verde)
- **Falsa Cor**: Realça estruturas específicas

## 🎓 Aplicações

Este projeto pode ser usado para:

1. **Pesquisa Astronômica**: Processamento de dados de observatórios
2. **Educação**: Ensino de processamento de imagem astronômica
3. **Análise de Dados**: Pipeline reutilizável para FITS
4. **Visualização**: Criação de imagens para publicação

## 🛠️ Desenvolvimento

### Adicionar Novo Método de Processamento

```python
# Em image_processor.py
@staticmethod
def seu_metodo(data: np.ndarray) -> np.ndarray:
    """Descrição do método"""
    result = data.copy()
    # Sua lógica aqui
    return result
```

### Adicionar Novo Colormap

```python
# Em rgb_converter.py
@staticmethod
def seu_colormap(channels: Dict[str, np.ndarray]) -> np.ndarray:
    """Descrição do seu colormap"""
    # Sua lógica de mapeamento
    return rgb
```

## 📊 Performance

Para imagens grandes (2K+):
- Use `smooth_kernel` para reduzir ruído
- Considere redimensionar para (512, 512) antes de processar
- Salve em PNG para melhor compressão

## ⚠️ Limitações e Considerações

- Arquivos FITS muito grandes podem exigir mais memória
- A qualidade depende dos dados de entrada
- Alguns métodos exigem que dados sejam normalizados

## 🔗 Referências

- [FITS Standard](https://fits.gsfc.nasa.gov/)
- [Astropy Documentation](https://docs.astropy.org/)
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)

## 📝 Licença

Este projeto é fornecido como-está para fins educacionais e de pesquisa.

## 👨‍💻 Autor

Erik Costa Souza - Engenheiro de Dados

---

**Versão**: 1.0.0  
**Última Atualização**: Novembro 2025

