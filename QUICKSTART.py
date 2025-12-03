#!/usr/bin/env python
"""
Quick Start - Astro Data Visualization
Exemplo rápido de como usar o pipeline
"""

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║   🌌 ASTRO DATA VISUALIZATION - QUICK START 🌌              ║
╚══════════════════════════════════════════════════════════════╝

Este script mostra como usar rapidamente o pipeline para
processar arquivos FITS e gerar imagens RGB.

══════════════════════════════════════════════════════════════

PASSO 1: Importar Módulos
─────────────────────────
>>> from src.pipeline import AstroDataVizPipeline
>>> from src.fits_reader import FITSReader

PASSO 2: Criar Pipeline
──────────────────────
>>> pipeline = AstroDataVizPipeline("data/processed")

PASSO 3: Processar um Arquivo FITS
──────────────────────────────────
>>> rgb, output_path = pipeline.process_fits_to_rgb(
...     "data/raw/meu_arquivo.fits",
...     output_name="minha_imagem"
... )

PASSO 4: Usar o Resultado
────────────────────────
>>> print(f"Salvo em: {output_path}")
>>> # A variável rgb contém a imagem numpy (H, W, 3)

══════════════════════════════════════════════════════════════

EXEMPLOS ADICIONAIS:
═══════════════════

1. Inspecionar um arquivo FITS:
─────────────────────────────
>>> with FITSReader("seu_arquivo.fits") as reader:
...     print(reader.get_info())
...     data = reader.get_primary_data()

2. Processar com diferentes opções:
──────────────────────────────────
>>> rgb, path = pipeline.process_fits_to_rgb(
...     "arquivo.fits",
...     output_name="resultado",
...     rgb_method="hubble"  # ou "natural"
... )

3. Processamento manual:
───────────────────────
>>> from src.image_processor import ImageProcessor
>>> from src.rgb_converter import RGBConverter

>>> # Carrega dados
>>> data = FITSReader("arquivo.fits").get_primary_data()

>>> # Processa
>>> processed = ImageProcessor.apply_pipeline(
...     data,
...     normalize_method="percentile",
...     stretch_method="asinh",
...     enhance=True
... )

>>> # Coloriza
>>> rgb = RGBConverter.colorize_monochrome(processed, "hot")

4. Gerar dados de teste:
───────────────────────
>>> from src.synthetic_fits_generator import create_test_fits_collection
>>> files = create_test_fits_collection("data/raw")

══════════════════════════════════════════════════════════════

EXECUTAR EXEMPLOS:
══════════════════

# Exemplo básico
$ python examples/example1_basic.py

# Múltiplas colorizações
$ python examples/example2_colorization.py

# Técnicas avançadas
$ python examples/example3_advanced.py

# Notebook interativo
$ jupyter notebook notebooks/astro_data_viz_demo.ipynb

══════════════════════════════════════════════════════════════

PARÂMETROS COMUNS:
══════════════════

ImageProcessor.apply_pipeline():
  • normalize_method: "minmax", "percentile", "zscore"
  • stretch_method: "asinh", "sqrt", "log"
  • enhance: True/False (realce de contraste)
  • smooth_kernel: int ou None (suavização)

RGBConverter.combine_channels():
  • weights: (r_weight, g_weight, b_weight)

RGBConverter.colorize_monochrome():
  • colormap: "hot", "cool", "plasma", "viridis", etc.

══════════════════════════════════════════════════════════════

DOCUMENTAÇÃO COMPLETA:
══════════════════════
Veja: README_PROJETO.md

══════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    main()
