"""
Pipeline completo de processamento FITS para RGB
"""

import numpy as np
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import logging
from PIL import Image

import fits_reader
import image_processor
import rgb_converter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AstroDataVizPipeline:
    """Pipeline de visualização de dados astronômicos"""
    
    def __init__(self, output_dir: str = "data/processed"):
        """
        Inicializa o pipeline
        
        Args:
            output_dir: Diretório de saída para imagens processadas
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data = {}
        
    def process_fits_to_rgb(self, 
                           fits_file: str,
                           output_name: Optional[str] = None,
                           rgb_method: str = "natural") -> Tuple[np.ndarray, str]:
        """
        Processa um arquivo FITS para RGB
        
        Args:
            fits_file: Caminho do arquivo FITS
            output_name: Nome do arquivo de saída (sem extensão)
            rgb_method: Método de conversão RGB
            
        Returns:
            Tupla (imagem_rgb, caminho_saída)
        """
        logger.info(f"Processando {fits_file}...")
        
        # Carrega FITS
        fits_path = Path(fits_file)
        if not output_name:
            output_name = fits_path.stem
        
        with fits_reader.FITSReader(fits_file) as reader:
            data = reader.get_primary_data()
            if data is None:
                logger.error("Nenhum dado encontrado no FITS")
                return None, None
            
            logger.info(f"Forma dos dados: {data.shape}")
        
        # Processa imagem
        if len(data.shape) == 2:
            # Monocromática - cria RGB a partir de um canal
            logger.info("Imagem monocromática detectada")
            processed = image_processor.ImageProcessor.apply_pipeline(data)
            rgb = rgb_converter.RGBConverter.create_from_single_channel(
                processed, colormap="hot"
            )
        else:
            # Multi-canal
            logger.info("Imagem multi-canal detectada")
            channels = self._extract_channels(data)
            rgb = self._combine_channels(channels, rgb_method)
        
        # Salva resultado
        output_path = self.output_dir / f"{output_name}.png"
        self._save_rgb_image(rgb, str(output_path))
        
        self.processed_data[output_name] = rgb
        return rgb, str(output_path)
    
    def process_multi_fits(self,
                          fits_files: List[str],
                          rgb_method: str = "natural",
                          channel_mapping: Optional[Dict[str, int]] = None) -> np.ndarray:
        """
        Processa múltiplos arquivos FITS para um único RGB
        
        Args:
            fits_files: Lista de caminhos FITS
            rgb_method: Método de combinação
            channel_mapping: Mapeamento de canais RGB para arquivos
            
        Returns:
            Imagem RGB combinada
        """
        if len(fits_files) < 3:
            logger.warning("Menos de 3 arquivos fornecidos, usando o mesmo arquivo para os 3 canais")
            fits_files = [fits_files[0]] * 3
        
        channels = {}
        
        for i, fits_file in enumerate(fits_files[:3]):
            with fits_reader.FITSReader(fits_file) as reader:
                data = reader.get_primary_data()
                if data is not None:
                    processed = image_processor.ImageProcessor.apply_pipeline(data)
                    channels[f"channel_{i}"] = processed
        
        if len(channels) < 3:
            logger.error("Não foi possível extrair 3 canais")
            return None
        
        channel_list = list(channels.values())
        rgb = rgb_converter.RGBConverter.combine_channels(
            channel_list[0], channel_list[1], channel_list[2]
        )
        
        return rgb
    
    def _extract_channels(self, data: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Extrai canais de dados multi-dimensionais
        
        Args:
            data: Array com múltiplas dimensões
            
        Returns:
            Dicionário com canais processados
        """
        channels = {}
        
        if len(data.shape) == 3:
            # Dados cúbicos (profundidade, altura, largura)
            for i in range(min(3, data.shape[0])):
                processed = image_processor.ImageProcessor.apply_pipeline(data[i])
                channels[f"channel_{i}"] = processed
        elif len(data.shape) == 2:
            # 2D - usa o mesmo canal três vezes
            processed = image_processor.ImageProcessor.apply_pipeline(data)
            channels["channel_0"] = processed
            channels["channel_1"] = processed
            channels["channel_2"] = processed
        
        return channels
    
    def _combine_channels(self, channels: Dict[str, np.ndarray], 
                         method: str = "natural") -> np.ndarray:
        """
        Combina canais em RGB
        
        Args:
            channels: Dicionário com canais
            method: Método de combinação
            
        Returns:
            Imagem RGB
        """
        channel_list = list(channels.values())
        
        if len(channel_list) < 3:
            logger.warning("Canais insuficientes, duplicando...")
            while len(channel_list) < 3:
                channel_list.append(channel_list[0])
        
        if method == "hubble":
            return rgb_converter.RGBConverter.combine_channels(
                channel_list[2], channel_list[1], channel_list[0]
            )
        else:  # natural
            return rgb_converter.RGBConverter.combine_channels(
                channel_list[0], channel_list[1], channel_list[2]
            )
    
    def _save_rgb_image(self, rgb: np.ndarray, output_path: str, 
                       quality: int = 95) -> None:
        """
        Salva imagem RGB em arquivo
        
        Args:
            rgb: Array RGB normalizado (0-1)
            output_path: Caminho de saída
            quality: Qualidade JPEG
        """
        # Converte para 0-255
        rgb_8bit = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
        
        # Cria imagem PIL
        image = Image.fromarray(rgb_8bit, mode='RGB')
        
        # Salva
        image.save(output_path, quality=quality)
        logger.info(f"Imagem salva em: {output_path}")
    
    def get_processed_image(self, name: str) -> Optional[np.ndarray]:
        """Obtém uma imagem processada do cache"""
        return self.processed_data.get(name)
    
    def list_processed_images(self) -> List[str]:
        """Lista todas as imagens processadas"""
        return list(self.processed_data.keys())


def process_fits(fits_file: str,
                output_dir: str = "data/processed",
                rgb_method: str = "natural") -> Tuple[np.ndarray, str]:
    """
    Função helper para processar um único arquivo FITS
    
    Args:
        fits_file: Arquivo FITS
        output_dir: Diretório de saída
        rgb_method: Método RGB
        
    Returns:
        Tupla (rgb_array, output_path)
    """
    pipeline = AstroDataVizPipeline(output_dir)
    return pipeline.process_fits_to_rgb(fits_file, rgb_method=rgb_method)
