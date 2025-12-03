"""
Módulo de conversão para RGB e colorização
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RGBConverter:
    """Conversor de dados astronômicos para RGB"""
    
    # Bandas típicas de observatórios
    TYPICAL_BANDS = {
        "HST": {  # Hubble Space Telescope
            "ultraviolet": 0.15,
            "blue": 0.43,
            "green": 0.55,
            "red": 0.65,
            "infrared": 0.8,
        },
        "JWST": {  # James Webb Space Telescope
            "f070w": 0.70,
            "f090w": 0.90,
            "f115w": 1.15,
            "f150w": 1.50,
            "f200w": 2.00,
        }
    }
    
    @staticmethod
    def combine_channels(red: np.ndarray, 
                        green: np.ndarray, 
                        blue: np.ndarray,
                        weights: Optional[Tuple[float, float, float]] = None) -> np.ndarray:
        """
        Combina três canais em uma imagem RGB
        
        Args:
            red: Canal vermelho
            green: Canal verde
            blue: Canal azul
            weights: Pesos para cada canal (padrão: 1, 1, 1)
            
        Returns:
            Imagem RGB com shape (height, width, 3)
        """
        if weights is None:
            weights = (1.0, 1.0, 1.0)
        
        # Garante que todos têm o mesmo tamanho
        shape = (max(red.shape[0], green.shape[0], blue.shape[0]),
                max(red.shape[1], green.shape[1], blue.shape[1]))
        
        r = RGBConverter._resize_to_shape(red, shape)
        g = RGBConverter._resize_to_shape(green, shape)
        b = RGBConverter._resize_to_shape(blue, shape)
        
        # Aplica pesos
        r = r * weights[0]
        g = g * weights[1]
        b = b * weights[2]
        
        # Normaliza novamente
        max_val = max(np.max(r), np.max(g), np.max(b))
        if max_val > 0:
            r = r / max_val
            g = g / max_val
            b = b / max_val
        
        # Stack em RGB
        rgb = np.stack([r, g, b], axis=2)
        return np.clip(rgb, 0, 1)
    
    @staticmethod
    def _resize_to_shape(data: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
        """Helper para redimensionar array para uma forma alvo"""
        from scipy import ndimage
        
        if data.shape != target_shape:
            zoom_factors = (
                target_shape[0] / data.shape[0],
                target_shape[1] / data.shape[1]
            )
            return ndimage.zoom(data, zoom_factors, order=1)
        return data
    
    @staticmethod
    def map_filters_to_rgb(filters: Dict[str, np.ndarray],
                          rgb_mapping: Dict[str, str]) -> np.ndarray:
        """
        Mapeia filtros/bandas astronômicas para RGB
        
        Args:
            filters: Dicionário com dados de diferentes filtros
            rgb_mapping: Dicionário mapeando 'red', 'green', 'blue' para nomes de filtros
            
        Returns:
            Imagem RGB (height, width, 3)
        """
        try:
            red = filters[rgb_mapping['red']]
            green = filters[rgb_mapping['green']]
            blue = filters[rgb_mapping['blue']]
            
            logger.info(f"Mapeamento RGB: R={rgb_mapping['red']}, "
                       f"G={rgb_mapping['green']}, B={rgb_mapping['blue']}")
            
            return RGBConverter.combine_channels(red, green, blue)
        except KeyError as e:
            logger.error(f"Filtro não encontrado no mapeamento: {e}")
            raise
    
    @staticmethod
    def hubble_palette(channels: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Cria uma imagem usando a paleta clássica do Hubble
        R=InfraRed, G=Red, B=Green
        
        Args:
            channels: Dicionário com canais de dados
            
        Returns:
            Imagem RGB
        """
        mapping = {
            'red': 'infrared',
            'green': 'red',
            'blue': 'green'
        }
        
        available_keys = list(channels.keys())
        if len(available_keys) >= 3:
            # Usa os três primeiros canais disponíveis
            mapping = {
                'red': available_keys[2],
                'green': available_keys[1],
                'blue': available_keys[0]
            }
        
        return RGBConverter.map_filters_to_rgb(channels, mapping)
    
    @staticmethod
    def natural_color(channels: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Cria uma imagem com cores naturais
        R=Red, G=Green, B=Blue
        
        Args:
            channels: Dicionário com canais de dados
            
        Returns:
            Imagem RGB
        """
        mapping = {
            'red': 'red',
            'green': 'green',
            'blue': 'blue'
        }
        
        available_keys = list(channels.keys())
        if len(available_keys) >= 3:
            mapping = {
                'red': available_keys[0],
                'green': available_keys[1],
                'blue': available_keys[2]
            }
        
        return RGBConverter.map_filters_to_rgb(channels, mapping)
    
    @staticmethod
    def colorize_monochrome(data: np.ndarray, colormap: str = "viridis") -> np.ndarray:
        """
        Coloriza uma imagem monocromática usando um colormap
        
        Args:
            data: Array 2D normalizado (0-1)
            colormap: Nome do colormap ('viridis', 'hot', 'cool', 'plasma', etc.)
            
        Returns:
            Imagem RGB colorizada
        """
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        
        cmap = cm.get_cmap(colormap)
        return cmap(data)[:, :, :3]  # Remove canal alpha
    
    @staticmethod
    def false_color_ir(channels: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Cria composição de falsa cor com infravermelha
        Útil para análise de vegetação e estruturas
        
        Args:
            channels: Dicionário com canais
            
        Returns:
            Imagem RGB de falsa cor
        """
        available_keys = list(channels.keys())
        
        if len(available_keys) >= 3:
            # NIR=R, Red=G, Green=B
            mapping = {
                'red': available_keys[2],      # Near-IR
                'green': available_keys[1],    # Red
                'blue': available_keys[0]      # Green
            }
            return RGBConverter.map_filters_to_rgb(channels, mapping)
        
        logger.warning("Canais insuficientes para composição de falsa cor IR")
        return None
    
    @staticmethod
    def create_from_single_channel(data: np.ndarray, 
                                  colormap: str = "hot") -> np.ndarray:
        """
        Cria uma imagem RGB a partir de um único canal monocromático
        
        Args:
            data: Array 2D normalizado
            colormap: Colormap a usar
            
        Returns:
            Imagem RGB
        """
        return RGBConverter.colorize_monochrome(data, colormap)
    
    @staticmethod
    def blend_channels(channel1: np.ndarray,
                      channel2: np.ndarray,
                      alpha: float = 0.5) -> np.ndarray:
        """
        Mistura dois canais com um fator alpha
        
        Args:
            channel1: Primeiro canal
            channel2: Segundo canal
            alpha: Fator de mistura (0-1)
            
        Returns:
            Canal misturado
        """
        return alpha * channel1 + (1 - alpha) * channel2
    
    @staticmethod
    def equalize_channels(red: np.ndarray,
                         green: np.ndarray,
                         blue: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Equaliza histogramas dos canais RGB para melhor equilíbrio
        
        Args:
            red, green, blue: Canais individuais
            
        Returns:
            Tupla com canais equalizados
        """
        from scipy import ndimage
        
        # Calcula mediana de cada canal
        medians = [np.nanmedian(red), np.nanmedian(green), np.nanmedian(blue)]
        target_median = np.median(medians)
        
        # Ajusta cada canal
        red = red * (target_median / (medians[0] + 1e-10))
        green = green * (target_median / (medians[1] + 1e-10))
        blue = blue * (target_median / (medians[2] + 1e-10))
        
        return np.clip(red, 0, 1), np.clip(green, 0, 1), np.clip(blue, 0, 1)


def create_rgb_image(channels: List[np.ndarray],
                    method: str = "natural",
                    weights: Optional[Tuple[float, float, float]] = None) -> np.ndarray:
    """
    Função helper para criar rapidamente uma imagem RGB
    
    Args:
        channels: Lista com três canais [red, green, blue]
        method: Método de combinação
        weights: Pesos para cada canal
        
    Returns:
        Imagem RGB
    """
    if len(channels) < 3:
        raise ValueError("Pelo menos 3 canais são necessários")
    
    return RGBConverter.combine_channels(channels[0], channels[1], channels[2], weights)
