# API Reference - Astro Data Visualization

## 📚 Referência Técnica Completa

### Módulo: fits_reader.py

#### Classe FITSReader

```python
class FITSReader:
    """Leitor de arquivos FITS astronômicos"""
    
    def __init__(self, filepath: str)
        # Inicializa o leitor
    
    def load(self) -> bool
        # Carrega arquivo FITS
        # Retorna: True se bem-sucedido
    
    def get_primary_data() -> np.ndarray
        # Obtém dados da HDU primária
    
    def get_extension_data(extension: int) -> np.ndarray
        # Obtém dados de extensão específica
    
    def get_all_data() -> Dict[str, np.ndarray]
        # Retorna todos os HDUs com dados
    
    def get_header(extension: int) -> fits.Header
        # Obtém header FITS
    
    def get_info() -> str
        # Retorna informações formatadas
    
    def close()
        # Fecha arquivo
    
    def __enter__ / __exit__
        # Suporta context manager
```

#### Funções Helper

```python
def load_fits(filepath: str) -> np.ndarray
    # Carrega rapidamente arquivo FITS
    # Retorna: Array numpy com dados

def load_fits_multi_channel(filepath: str, 
                           channels: List[int] = None) -> Dict[str, np.ndarray]
    # Carrega múltiplos canais
```

---

### Módulo: image_processor.py

#### Classe ImageProcessor

**Normalização:**
```python
@staticmethod
def normalize(data: np.ndarray, 
             method: str = "minmax") -> np.ndarray
    # Métodos: "minmax", "percentile", "zscore"
    # Retorna: Array normalizado [0, 1]
```

**Stretching:**
```python
@staticmethod
def asinh_stretch(data: np.ndarray, 
                 scale: float = 0.1) -> np.ndarray
    # Stretching inverse hyperbolic sine

@staticmethod
def sqrt_stretch(data: np.ndarray) -> np.ndarray
    # Stretching raiz quadrada

@staticmethod
def log_stretch(data: np.ndarray) -> np.ndarray
    # Stretching logarítmico
```

**Processamento:**
```python
@staticmethod
def enhance_contrast(data: np.ndarray, 
                    sigma: float = 1.0) -> np.ndarray
    # Realça contraste adaptativo

@staticmethod
def smooth(data: np.ndarray, 
          kernel_size: int = 3) -> np.ndarray
    # Suaviza com median filter

@staticmethod
def sharpen(data: np.ndarray, 
           amount: float = 0.5) -> np.ndarray
    # Aguça a imagem

@staticmethod
def resize(data: np.ndarray, 
          output_shape: Tuple[int, int]) -> np.ndarray
    # Redimensiona imagem

@staticmethod
def handle_nan(data: np.ndarray, 
              method: str = "zero") -> np.ndarray
    # Trata valores NaN
    # Métodos: "zero", "mean", "median", "interpolate"

@staticmethod
def remove_outliers(data: np.ndarray, 
                   threshold: float = 3.0) -> np.ndarray
    # Remove outliers por desvio padrão

@staticmethod
def apply_pipeline(data: np.ndarray, 
                  normalize_method: str = "percentile",
                  stretch_method: str = "asinh",
                  enhance: bool = True,
                  smooth_kernel: Optional[int] = None) -> np.ndarray
    # Pipeline completo de processamento
```

---

### Módulo: rgb_converter.py

#### Classe RGBConverter

**Combinação de Canais:**
```python
@staticmethod
def combine_channels(red: np.ndarray,
                    green: np.ndarray,
                    blue: np.ndarray,
                    weights: Optional[Tuple] = None) -> np.ndarray
    # Combina 3 canais em RGB
    # weights: (r_weight, g_weight, b_weight)
    # Retorna: Array (H, W, 3) [0, 1]

@staticmethod
def map_filters_to_rgb(filters: Dict[str, np.ndarray],
                      rgb_mapping: Dict[str, str]) -> np.ndarray
    # Mapeia filtros nomeados para RGB
```

**Paletas e Colormaps:**
```python
@staticmethod
def hubble_palette(channels: Dict[str, np.ndarray]) -> np.ndarray
    # Paleta clássica Hubble: R=IR, G=Red, B=Green

@staticmethod
def natural_color(channels: Dict[str, np.ndarray]) -> np.ndarray
    # Cores naturais: R=Red, G=Green, B=Blue

@staticmethod
def false_color_ir(channels: Dict[str, np.ndarray]) -> np.ndarray
    # Falsa cor infravermelha

@staticmethod
def colorize_monochrome(data: np.ndarray,
                       colormap: str = "viridis") -> np.ndarray
    # Coloriza imagem monocromática
    # colormaps: "hot", "cool", "plasma", "viridis", etc.

@staticmethod
def create_from_single_channel(data: np.ndarray,
                              colormap: str = "hot") -> np.ndarray
    # Cria RGB de um único canal monocromático
```

**Processamento de Canais:**
```python
@staticmethod
def blend_channels(channel1: np.ndarray,
                  channel2: np.ndarray,
                  alpha: float = 0.5) -> np.ndarray
    # Mistura dois canais com alpha

@staticmethod
def equalize_channels(red: np.ndarray,
                     green: np.ndarray,
                     blue: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]
    # Equaliza histogramas dos canais
```

#### Funções Helper

```python
def create_rgb_image(channels: List[np.ndarray],
                    method: str = "natural",
                    weights: Optional[Tuple] = None) -> np.ndarray
    # Cria imagem RGB rapidamente
```

---

### Módulo: pipeline.py

#### Classe AstroDataVizPipeline

```python
class AstroDataVizPipeline:
    """Pipeline completo de processamento"""
    
    def __init__(self, output_dir: str = "data/processed")
        # Inicializa pipeline
    
    def process_fits_to_rgb(fits_file: str,
                           output_name: Optional[str] = None,
                           rgb_method: str = "natural") -> Tuple[np.ndarray, str]
        # Processa arquivo FITS → RGB
        # Retorna: (imagem_rgb, caminho_saída)
    
    def process_multi_fits(fits_files: List[str],
                          rgb_method: str = "natural",
                          channel_mapping: Optional[Dict] = None) -> np.ndarray
        # Processa múltiplos FITS → RGB único
    
    def get_processed_image(name: str) -> Optional[np.ndarray]
        # Obtém imagem processada do cache
    
    def list_processed_images() -> List[str]
        # Lista todas as imagens processadas
```

#### Funções Helper

```python
def process_fits(fits_file: str,
                output_dir: str = "data/processed",
                rgb_method: str = "natural") -> Tuple[np.ndarray, str]
    # Função wrapper rápida
```

---

### Módulo: synthetic_fits_generator.py

```python
def create_synthetic_image(shape: Tuple[int, int] = (512, 512),
                          objects: List[dict] = None) -> np.ndarray
    # Cria imagem astronômica sintética

def create_multiband_fits(output_path: str,
                         shape: Tuple[int, int] = (512, 512),
                         n_bands: int = 3) -> None
    # Cria arquivo FITS multi-banda sintético

def create_monochrome_fits(output_path: str,
                          shape: Tuple[int, int] = (512, 512)) -> None
    # Cria arquivo FITS monocromático sintético

def create_test_fits_collection(output_dir: str = "data/raw") -> List[str]
    # Cria coleção de arquivos para testes
```

---

## 📊 Tipos de Dados

### Arrays Esperados

**Entrada (FITS brutos):**
- 2D: `(height, width)` - Valores podem ser negativos ou muito grandes
- 3D: `(depth, height, width)` - Múltiplos canais

**Após Normalização:**
- Range: `[0, 1]`
- dtype: `float32` ou `float64`

**Saída RGB:**
- Shape: `(height, width, 3)`
- Range: `[0, 1]`
- dtype: `float32` ou `float64`
- Pode ser convertido para `uint8` (0-255) para PNG

---

## 🔄 Fluxo Típico

```
FITS Bruto (2D/3D)
        ↓
    Carregamento (FITSReader)
        ↓
    Tratamento de NaN
        ↓
    Normalização
        ↓
    Stretching (Asinh/Log/Sqrt)
        ↓
    Realce de Contraste
        ↓
    Suavização (opcional)
        ↓
    Combinação RGB (ou Colorização)
        ↓
    Conversão para 8-bit
        ↓
    Salvamento (PNG)
```

---

## 💾 Formatos de Entrada/Saída

**Entrada:**
- FITS (`.fits`, `.fit`)
- Suporta HDU primária e extensões
- Qualquer número de bandas

**Saída:**
- PNG (recomendado)
- JPEG (com perda)
- Array numpy (processado)

---

## ⚙️ Configurações Recomendadas

### Para Dados com Grande Dinâmica
```python
ImageProcessor.apply_pipeline(
    data,
    normalize_method="percentile",
    stretch_method="asinh",
    enhance=True,
    smooth_kernel=None
)
```

### Para Dados Ruidosos
```python
ImageProcessor.apply_pipeline(
    data,
    normalize_method="percentile",
    stretch_method="sqrt",
    enhance=False,
    smooth_kernel=5
)
```

### Para Detalhes Finos
```python
ImageProcessor.apply_pipeline(
    data,
    normalize_method="minmax",
    stretch_method="log",
    enhance=True,
    smooth_kernel=None
)
```

---

## 🧪 Testes

```bash
# Todos os testes
pytest tests/ -v

# Cobertura
pytest tests/ --cov=src

# Teste específico
pytest tests/test_fits_reader.py::TestFITSReader::test_load_monochrome
```

---

## 📈 Performance

| Operação | Tempo (512x512) | Memória |
|----------|-----------------|---------|
| Carregar FITS | ~10ms | ~2MB |
| Normalizar | ~5ms | ~2MB |
| Stretching | ~10ms | ~2MB |
| Realce | ~15ms | ~2MB |
| Combinar RGB | ~5ms | ~3MB |
| Total | ~50ms | ~11MB |

---

## 🐛 Troubleshooting

### "Import numpy could not be resolved"
→ Execute: `pip install -r requirements.txt`

### "FITS file not found"
→ Verifique o caminho absoluto do arquivo

### "No data found in FITS"
→ O arquivo pode estar corrupto ou vazio

### "Shape mismatch in combine_channels"
→ Use diferentes canais com resize automático ativo

---

**Versão**: 1.0.0  
**Última Atualização**: Novembro 2025
