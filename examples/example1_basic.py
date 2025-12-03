"""
Exemplo 1: Processamento de arquivo FITS sintético simples
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from synthetic_fits_generator import create_test_fits_collection
from pipeline import AstroDataVizPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Exemplo de processamento básico"""
    
    logger.info("=== Exemplo 1: Processamento FITS Básico ===\n")
    
    # Cria dados de teste
    logger.info("Gerando arquivos FITS sintéticos...")
    fits_files = create_test_fits_collection("data/raw")
    logger.info(f"Arquivos criados: {len(fits_files)}\n")
    
    # Cria o pipeline
    pipeline = AstroDataVizPipeline("data/processed")
    
    # Processa um arquivo monocromático
    logger.info("Processando arquivo monocromático...")
    rgb1, path1 = pipeline.process_fits_to_rgb(
        "data/raw/synthetic_monochrome.fits",
        output_name="example1_monochrome"
    )
    print(f"Saída: {path1}\n")
    
    # Processa arquivo multi-banda
    logger.info("Processando arquivo multi-banda...")
    rgb2, path2 = pipeline.process_fits_to_rgb(
        "data/raw/synthetic_multiband.fits",
        output_name="example1_multiband"
    )
    print(f"Saída: {path2}\n")
    
    logger.info("Exemplo 1 concluído!")


if __name__ == "__main__":
    main()
