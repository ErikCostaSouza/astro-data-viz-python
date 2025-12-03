"""
Exemplo 2: Processamento multi-arquivo com diferentes estratégias de colorização
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from synthetic_fits_generator import create_test_fits_collection
from pipeline import AstroDataVizPipeline
from fits_reader import FITSReader
from image_processor import ImageProcessor
from rgb_converter import RGBConverter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Exemplo de diferentes métodos de conversão RGB"""
    
    logger.info("=== Exemplo 2: Múltiplos Métodos de Colorização ===\n")
    
    # Cria dados de teste
    fits_files = create_test_fits_collection("data/raw")
    
    # Cria pipeline
    pipeline = AstroDataVizPipeline("data/processed")
    
    # Carrega 3 arquivos para simular 3 bandas
    channels = []
    band_names = ["ultraviolet", "blue", "green", "red", "infrared"]
    
    for i, name in enumerate(band_names[:3]):
        fits_path = f"data/raw/synthetic_band_{name}.fits"
        
        with FITSReader(fits_path) as reader:
            data = reader.get_primary_data()
            if data is not None:
                # Processa cada canal
                processed = ImageProcessor.apply_pipeline(
                    data,
                    normalize_method="percentile",
                    stretch_method="asinh",
                    enhance=True
                )
                channels.append(processed)
                logger.info(f"Processado: {name}")
    
    if len(channels) == 3:
        # Método 1: Cores naturais
        logger.info("\nCriando composição de cor natural...")
        rgb_natural = RGBConverter.combine_channels(
            channels[0], channels[1], channels[2]
        )
        pipeline._save_rgb_image(rgb_natural, "data/processed/example2_natural.png")
        
        # Método 2: Paleta Hubble (invertida)
        logger.info("Criando composição Hubble-like...")
        rgb_hubble = RGBConverter.combine_channels(
            channels[2], channels[1], channels[0]
        )
        pipeline._save_rgb_image(rgb_hubble, "data/processed/example2_hubble.png")
        
        # Método 3: Falsa cor com pesos
        logger.info("Criando composição de falsa cor...")
        rgb_false = RGBConverter.combine_channels(
            channels[2], channels[1], channels[0],
            weights=(1.5, 1.0, 0.5)
        )
        pipeline._save_rgb_image(rgb_false, "data/processed/example2_falsecolor.png")
        
        # Método 4: Monocromática com diferentes colormaps
        logger.info("Criando composições monocromáticas com colormaps...")
        for colormap in ["hot", "viridis", "plasma", "cool"]:
            rgb_mono = RGBConverter.colorize_monochrome(channels[0], colormap)
            pipeline._save_rgb_image(
                rgb_mono, 
                f"data/processed/example2_mono_{colormap}.png"
            )
    
    logger.info("\nExemplo 2 concluído!")


if __name__ == "__main__":
    main()
