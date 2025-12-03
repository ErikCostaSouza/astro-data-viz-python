"""
Exemplo 3: Análise e visualização avançada com diferentes técnicas de processamento
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from synthetic_fits_generator import create_monochrome_fits
from fits_reader import FITSReader
from image_processor import ImageProcessor
from rgb_converter import RGBConverter
from pipeline import AstroDataVizPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Exemplo de técnicas avançadas de processamento"""
    
    logger.info("=== Exemplo 3: Técnicas Avançadas de Processamento ===\n")
    
    # Cria uma imagem de teste
    test_file = "data/raw/synthetic_advanced.fits"
    create_monochrome_fits(test_file, shape=(512, 512))
    
    # Carrega os dados
    with FITSReader(test_file) as reader:
        raw_data = reader.get_primary_data()
    
    pipeline = AstroDataVizPipeline("data/processed")
    
    logger.info("Testando diferentes técnicas de stretching...\n")
    
    # 1. Normalização diferentes
    norm_methods = ["minmax", "percentile", "zscore"]
    for method in norm_methods:
        normalized = ImageProcessor.normalize(raw_data, method=method)
        rgb = RGBConverter.colorize_monochrome(normalized, "viridis")
        pipeline._save_rgb_image(
            rgb,
            f"data/processed/example3_normalize_{method}.png"
        )
        logger.info(f"Normalização {method}: salvo")
    
    # 2. Diferentes stretches
    normalized = ImageProcessor.normalize(raw_data, method="percentile")
    
    stretches = {
        "asinh": ImageProcessor.asinh_stretch,
        "sqrt": ImageProcessor.sqrt_stretch,
        "log": ImageProcessor.log_stretch,
    }
    
    for name, func in stretches.items():
        stretched = func(normalized)
        rgb = RGBConverter.colorize_monochrome(stretched, "hot")
        pipeline._save_rgb_image(
            rgb,
            f"data/processed/example3_stretch_{name}.png"
        )
        logger.info(f"Stretch {name}: salvo")
    
    # 3. Realce de contraste
    logger.info("\nTestando realce de contraste...")
    enhanced = ImageProcessor.enhance_contrast(normalized, sigma=1.0)
    rgb = RGBConverter.colorize_monochrome(enhanced, "plasma")
    pipeline._save_rgb_image(rgb, "data/processed/example3_enhanced.png")
    
    # 4. Suavização e aguçamento
    logger.info("Testando suavização...")
    smoothed = ImageProcessor.smooth(normalized, kernel_size=5)
    rgb = RGBConverter.colorize_monochrome(smoothed, "cool")
    pipeline._save_rgb_image(rgb, "data/processed/example3_smoothed.png")
    
    logger.info("Testando aguçamento...")
    sharpened = ImageProcessor.sharpen(normalized, amount=0.8)
    rgb = RGBConverter.colorize_monochrome(sharpened, "viridis")
    pipeline._save_rgb_image(rgb, "data/processed/example3_sharpened.png")
    
    # 5. Pipeline completo
    logger.info("\nAplicando pipeline completo...")
    pipeline_result = ImageProcessor.apply_pipeline(
        raw_data,
        normalize_method="percentile",
        stretch_method="asinh",
        enhance=True,
        smooth_kernel=3
    )
    rgb = RGBConverter.colorize_monochrome(pipeline_result, "hot")
    pipeline._save_rgb_image(rgb, "data/processed/example3_full_pipeline.png")
    
    logger.info("\nExemplo 3 concluído!")


if __name__ == "__main__":
    main()
