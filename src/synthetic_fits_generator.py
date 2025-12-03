"""
Gerador de dados FITS sintéticos para testes e exemplos
"""

import numpy as np
from astropy.io import fits
from pathlib import Path
from typing import Tuple, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_synthetic_image(shape: Tuple[int, int] = (512, 512),
                          objects: List[dict] = None) -> np.ndarray:
    """
    Cria uma imagem sintética simulando dados astronômicos
    
    Args:
        shape: Dimensões da imagem (altura, largura)
        objects: Lista de objetos astronômicos a simular
        
    Returns:
        Array com dados de imagem
    """
    image = np.zeros(shape)
    
    # Background com gradiente suave
    y, x = np.ogrid[:shape[0], :shape[1]]
    background = np.exp(-(((x - shape[1]//2)**2 + (y - shape[0]//2)**2) / (2 * (max(shape)//3)**2)))
    image += background * 100
    
    # Ruído de fundo
    image += np.random.normal(10, 2, shape)
    
    if objects:
        for obj in objects:
            add_synthetic_object(image, obj)
    else:
        # Adiciona alguns objetos padrão
        add_synthetic_object(image, {
            "type": "star",
            "center": (shape[0]//4, shape[1]//4),
            "brightness": 1000
        })
        add_synthetic_object(image, {
            "type": "nebula",
            "center": (3*shape[0]//4, 3*shape[1]//4),
            "radius": 50,
            "brightness": 500
        })
        add_synthetic_object(image, {
            "type": "galaxy",
            "center": (shape[0]//2, shape[1]//2),
            "radius": 80,
            "brightness": 400
        })
    
    # Clipa valores negativos
    image = np.clip(image, 0, np.inf)
    
    return image


def add_synthetic_object(image: np.ndarray, obj: dict) -> None:
    """
    Adiciona um objeto astronômico sintético à imagem
    
    Args:
        image: Array da imagem
        obj: Dicionário com propriedades do objeto
    """
    obj_type = obj.get("type", "star")
    center = obj.get("center", (image.shape[0]//2, image.shape[1]//2))
    brightness = obj.get("brightness", 1000)
    
    y, x = np.ogrid[:image.shape[0], :image.shape[1]]
    cy, cx = center
    
    if obj_type == "star":
        # Estrela como PSF gaussiana
        sigma = 2
        gaussian = brightness * np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * sigma**2))
        image += gaussian
        
    elif obj_type == "nebula":
        # Nebulosa como blob suave
        radius = obj.get("radius", 30)
        nebula = brightness * np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * radius**2))
        image += nebula
        
    elif obj_type == "galaxy":
        # Galáxia como estrutura espiral
        radius = obj.get("radius", 50)
        disk = brightness * np.exp(-np.sqrt((x - cx)**2 + (y - cy)**2) / radius)
        image += disk


def create_multiband_fits(output_path: str,
                         shape: Tuple[int, int] = (512, 512),
                         n_bands: int = 3) -> None:
    """
    Cria um arquivo FITS multi-banda sintético
    
    Args:
        output_path: Caminho do arquivo de saída
        shape: Dimensões das imagens
        n_bands: Número de bandas
    """
    # Cria HDU primária
    primary_hdu = fits.PrimaryHDU()
    
    # Adiciona imagens sintéticas em diferentes "comprimentos de onda"
    hdus = [primary_hdu]
    
    for i in range(n_bands):
        # Varia os parâmetros para simular diferentes bandas
        wavelength = 0.4 + i * 0.2  # Simula UV->Blue->Red->IR
        brightness_factor = 1 + 0.3 * i
        
        image = create_synthetic_image(shape)
        image = image * brightness_factor
        
        # Adiciona mais estrutura para bandas do IR
        if i > 1:
            image += create_synthetic_image(shape, objects=[{
                "type": "galaxy",
                "center": (shape[0]//3, shape[1]//3),
                "radius": 60,
                "brightness": 200
            }])
        
        image = np.clip(image, 0, np.inf)
        
        # Cria ImageHDU
        image_hdu = fits.ImageHDU(data=image.astype(np.float32), name=f"BAND_{i}")
        image_hdu.header['WAVELENGTH'] = (wavelength, 'Wavelength in micrometers')
        image_hdu.header['DESCRIP'] = f'Band {i} data'
        
        hdus.append(image_hdu)
    
    # Salva o arquivo
    hdul = fits.HDUList(hdus)
    hdul.writeto(output_path, overwrite=True)
    logger.info(f"Arquivo FITS sintético criado: {output_path}")


def create_monochrome_fits(output_path: str,
                          shape: Tuple[int, int] = (512, 512)) -> None:
    """
    Cria um arquivo FITS monocromático sintético
    
    Args:
        output_path: Caminho do arquivo de saída
        shape: Dimensões da imagem
    """
    image = create_synthetic_image(shape)
    image = image.astype(np.float32)
    
    hdu = fits.PrimaryHDU(data=image)
    hdu.header['TELESCOP'] = 'SYNTHETIC'
    hdu.header['INSTRUME'] = 'SIMULATOR'
    hdu.header['NAXIS'] = 2
    
    hdu.writeto(output_path, overwrite=True)
    logger.info(f"Arquivo FITS monocromático criado: {output_path}")


def create_test_fits_collection(output_dir: str = "data/raw") -> List[str]:
    """
    Cria uma coleção de arquivos FITS sintéticos para testes
    
    Args:
        output_dir: Diretório de saída
        
    Returns:
        Lista com caminhos dos arquivos criados
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    files = []
    
    # Multi-banda
    multi_path = Path(output_dir) / "synthetic_multiband.fits"
    create_multiband_fits(str(multi_path), shape=(512, 512), n_bands=3)
    files.append(str(multi_path))
    
    # Monocromático
    mono_path = Path(output_dir) / "synthetic_monochrome.fits"
    create_monochrome_fits(str(mono_path))
    files.append(str(mono_path))
    
    # Vários monocromáticos para simular diferentes bandas
    band_names = ["ultraviolet", "blue", "green", "red", "infrared"]
    for name in band_names:
        band_path = Path(output_dir) / f"synthetic_band_{name}.fits"
        create_monochrome_fits(str(band_path))
        files.append(str(band_path))
    
    logger.info(f"Coleção de teste criada em {output_dir}")
    return files


if __name__ == "__main__":
    # Cria arquivos de teste
    create_test_fits_collection()
