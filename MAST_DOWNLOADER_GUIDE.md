# 📡 Guia: Baixando Dados Reais do MAST

## 🚀 Uso Rápido

### 1️⃣ Instalar Dependência

```bash
pip install astroquery
```

### 2️⃣ Baixar Dados do Hubble

```bash
# Básico (M51 - default)
python download_mast_data.py

# Especificar alvo
python download_mast_data.py --target "NGC 6543"

# Limitar quantidade
python download_mast_data.py --target "M31" --limit 5
```

### 3️⃣ Baixar Dados do JWST

```bash
python download_mast_data.py --source jwst

# Especificar alvo
python download_mast_data.py --source jwst --target "CEERS"
```

### 4️⃣ Baixar de Ambos + Processar

```bash
python download_mast_data.py --source both --process
```

---

## 📋 Opções Completas

```
--source     : hubble | jwst | both                 (default: hubble)
--target     : Nome do alvo                         (ex: M51, NGC6543)
--limit      : Número máximo de arquivos            (default: 3)
--output     : Diretório de saída                   (default: ./data/raw)
--process    : Processa com pipeline                (default: False)
```

---

## 🎯 Alvos Recomendados

### Hubble (HST)
| Alvo | Tipo | Descrição |
|------|------|-----------|
| **M51** | Galáxia | Clássica galáxia "Whirlpool" |
| **NGC 6543** | Nebulosa | Nebulosa planetária em forma de olho |
| **M31** | Galáxia | Andrômeda |
| **Hubble Deep Field** | Campo profundo | Imagens icônicas |
| **M87** | Galáxia | Centro de aglomerado |

### JWST
| Alvo | Tipo | Descrição |
|------|------|-----------|
| **CEERS** | Survey | Cosmic Evolution Early Release Science |
| **GN-COSMOS** | Campo profundo | Cosmological field |
| **ERGs** | Galáxias | Extremely Red Galaxies |
| **CANDELS** | Survey | Cosmic Assembly Near-infrared Deep |

---

## 💡 Exemplos Completos

### Exemplo 1: M51 com Processamento
```bash
python download_mast_data.py \
    --target "M51" \
    --limit 3 \
    --process
```
**Resultado**: Baixa 3 imagens de M51, inspeciona e gera PNGs processadas

### Exemplo 2: NGC 6543 (Nebulosa)
```bash
python download_mast_data.py \
    --target "NGC 6543" \
    --limit 5
```

### Exemplo 3: JWST com Limite Maior
```bash
python download_mast_data.py \
    --source jwst \
    --target "CEERS" \
    --limit 10 \
    --output "./data/jwst_raw"
```

### Exemplo 4: Ambos os Telescópios
```bash
python download_mast_data.py \
    --source both \
    --process
```

---

## 📊 O que Acontece

### Fluxo de Execução

```
1. Conecta ao MAST Archive
   ↓
2. Busca observações por alvo
   ↓
3. Filtra apenas FITS de HST/JWST
   ↓
4. Baixa N primeiros arquivos
   ↓
5. Renomeia para organização
   ↓
6. [OPCIONAL] Processa com seu pipeline
   ↓
7. Salva em ./data/raw e ./data/processed
```

### Output Esperado

```
🔍 Procurando por imagens do Hubble: M51
✅ Encontradas 150 observações
✅ 45 observações do Hubble disponíveis

📥 Baixando observação 1/3...
   Data: HST_01234567_001_WFC3_UVIS
   Instrumento: WFC3/UVIS
   ✅ Salvo: hubble_M51_1.fits

📥 Baixando observação 2/3...
   ✅ Salvo: hubble_M51_2.fits

✅ Total baixado: 3 arquivo(s)

📋 Inspecionando: hubble_M51_1.fits
   Shape: (4096, 4096)
   Tipo: float32
   Min: 100.0
   Max: 15000.0
```

---

## 🔧 Uso em Python

Se quiser usar diretamente no seu código:

```python
from download_mast_data import download_hubble_data, process_downloaded_data

# Baixa dados
files = download_hubble_data(target="M51", limit=3)

# Processa
for filepath in files:
    output = process_downloaded_data(filepath)
    print(f"Processado: {output}")
```

---

## ⚠️ Troubleshooting

### Erro: "astroquery não encontrado"
```bash
pip install astroquery
```

### Erro: "Nenhuma observação encontrada"
- Verifique a ortografia do alvo
- Tente alvos conhecidos: M51, NGC 6543, M87
- O MAST pode ter downtime

### Downloads Lentos
- MAST pode ter fila de requisições
- Reduza `--limit` para testar
- Tente em horários fora de pico

### Arquivos Muito Grandes
- Alguns arquivos FITS podem ter 100MB+
- Use `--limit 1` para testar
- Considere aumentar espaço em disco

---

## 📚 Mais Informações

- **MAST**: https://archive.stsci.edu/
- **Astroquery Docs**: https://astroquery.readthedocs.io/
- **HST Handbook**: https://www.stsci.edu/hst/HST_overview
- **JWST Data**: https://jwst-docs.stsci.edu/

---

## 🎓 Integração com seu Pipeline

Os arquivos baixados funcionam perfeitamente com seu pipeline existente:

```python
# Em example4_real_data.py
from src.fits_reader import FITSReader
from src.image_processor import ImageProcessor
from src.rgb_converter import RGBConverter
from src.pipeline import AstroDataVizPipeline

# Use qualquer arquivo FITS baixado
pipeline = AstroDataVizPipeline("./data/processed")

# Process como você já faz
result = pipeline.process_fits_to_rgb(
    "./data/raw/hubble_M51_1.fits",
    output_name="m51_processed"
)

if result:
    rgb_image, filepath = result
    print(f"✅ Imagem salva: {filepath}")
```

---

## ✅ Checklist

- [ ] Instalou astroquery: `pip install astroquery`
- [ ] Testou download simples: `python download_mast_data.py`
- [ ] Verificou arquivos em `./data/raw/`
- [ ] Processou com `--process` flag
- [ ] Verificou saída em `./data/processed/`
- [ ] Testou com diferentes alvos
- [ ] Integrou com seu pipeline

---

**Pronto para explorar dados reais de telescópios espaciais! 🌌**
