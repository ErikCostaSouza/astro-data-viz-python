"""
Módulo de processamento de imagens astronômicas
"""

import numpy as np
from scipy import ndimage
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageProcessor:
    """Processador de imagens astronômicas"""
    
    @staticmethod
    def normalize(data: np.ndarray, method: str = "minmax") -> np.ndarray:
        """
        Normaliza os dados para o intervalo [0, 1]
        
        Args:
            data: Array de dados
            method: Método de normalização ('minmax', 'percentile', 'zscore')
            
        Returns:
            Array normalizado
        """
        if method == "minmax":
            vmin, vmax = np.nanmin(data), np.nanmax(data)
            if vmax > vmin:
                return (data - vmin) / (vmax - vmin)
        
        elif method == "percentile":
            # Usa percentis 1% e 99%
            vmin, vmax = np.nanpercentile(data, [1, 99])
            normalized = (data - vmin) / (vmax - vmin)
            return np.clip(normalized, 0, 1)
        
        elif method == "zscore":
            # Normaliza por z-score
            mean = np.nanmean(data)
            std = np.nanstd(data)
            if std > 0:
                return (data - mean) / (3 * std) + 0.5
            return data
        
        return np.clip(data, 0, 1)
    
    @staticmethod
    def asinh_stretch(data: np.ndarray, scale: float = 0.1) -> np.ndarray:
        """
        Aplica stretching asinh (inverse hyperbolic sine)
        Útil para dados com grande dinâmica
        
        Args:
            data: Array de dados (deve estar normalizado entre 0-1)
            scale: Fator de escala
            
        Returns:
            Array com stretching aplicado
        """
        normalized = ImageProcessor.normalize(data)
        return np.arcsinh(normalized / scale) / np.arcsinh(1 / scale)
    
    @staticmethod
    def sqrt_stretch(data: np.ndarray) -> np.ndarray:
        """
        Aplica stretching raiz quadrada
        
        Args:
            data: Array de dados normalizado
            
        Returns:
            Array com stretching raiz quadrada
        """
        normalized = ImageProcessor.normalize(data)
        return np.sqrt(normalized)
    
    @staticmethod
    def log_stretch(data: np.ndarray) -> np.ndarray:
        """
        Aplica stretching logarítmico
        
        Args:
            data: Array de dados normalizado
            
        Returns:
            Array com stretching logarítmico
        """
        normalized = ImageProcessor.normalize(data)
        return np.log1p(normalized) / np.log1p(1)
    
    @staticmethod
    def enhance_contrast(data: np.ndarray, sigma: float = 1.0) -> np.ndarray:
        """
        Aumenta o contraste usando adaptative histogram equalization
        
        Args:
            data: Array de dados normalizado
            sigma: Sigma para Gaussian blur
            
        Returns:
            Array com contraste aumentado
        """
        # Gaussian blur para referência
        blurred = ndimage.gaussian_filter(data, sigma=sigma)
        
        # Diferença: detalhes locais
        details = data - blurred
        
        # Combina imagem original com detalhes amplificados
        enhanced = data + 0.5 * details
        
        return np.clip(enhanced, 0, 1)
    
    @staticmethod
    def remove_outliers(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
        """
        Remove outliers usando desvio padrão
        
        Args:
            data: Array de dados
            threshold: Multiplicador de desvio padrão
            
        Returns:
            Array com outliers removidos
        """
        mean = np.nanmean(data)
        std = np.nanstd(data)
        
        # Cria máscara para valores válidos
        valid_mask = np.abs(data - mean) <= threshold * std
        
        # Replace outliers com NaN
        result = data.copy().astype(float)
        result[~valid_mask] = np.nan
        
        # Interpola NaNs
        result = ndimage.median_filter(result, size=3)
        
        return result
    
    @staticmethod
    def smooth(data: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Suaviza a imagem usando median filter
        
        Args:
            data: Array de dados
            kernel_size: Tamanho do kernel
            
        Returns:
            Array suavizado
        """
        return ndimage.median_filter(data, size=kernel_size)
    
    @staticmethod
    def sharpen(data: np.ndarray, amount: float = 0.5) -> np.ndarray:
        """
        Aguça a imagem
        
        Args:
            data: Array de dados normalizado
            amount: Quantidade de aguçamento
            
        Returns:
            Array aguçado
        """
        blurred = ndimage.gaussian_filter(data, sigma=1.0)
        sharpened = data + amount * (data - blurred)
        return np.clip(sharpened, 0, 1)
    
    @staticmethod
    def resize(data: np.ndarray, output_shape: Tuple[int, int]) -> np.ndarray:
        """
        Redimensiona a imagem usando zoom
        
        Args:
            data: Array de dados 2D
            output_shape: Forma de saída (height, width)
            
        Returns:
            Array redimensionado
        """
        zoom_factors = (
            output_shape[0] / data.shape[0],
            output_shape[1] / data.shape[1]
        )
        return ndimage.zoom(data, zoom_factors, order=1)
    
    @staticmethod
    def handle_nan(data: np.ndarray, method: str = "zero") -> np.ndarray:
        """
        Trata valores NaN
        
        Args:
            data: Array de dados
            method: 'zero', 'mean', 'median', 'interpolate'
            
        Returns:
            Array sem NaN
        """
        result = data.copy()
        nan_mask = np.isnan(result)
        
        if not np.any(nan_mask):
            return result
        
        if method == "zero":
            result[nan_mask] = 0
        elif method == "mean":
            result[nan_mask] = np.nanmean(result)
        elif method == "median":
            result[nan_mask] = np.nanmedian(result)
        elif method == "interpolate":
            result = ndimage.median_filter(result, size=3)
        
        return result
    
    @staticmethod
    def apply_pipeline(data: np.ndarray, 
                      normalize_method: str = "percentile",
                      stretch_method: str = "asinh",
                      enhance: bool = True,
                      smooth_kernel: Optional[int] = None) -> np.ndarray:
        """
        Aplica um pipeline completo de processamento
        
        Args:
            data: Array de dados brutos
            normalize_method: Método de normalização
            stretch_method: Método de stretching
            enhance: Se deve aplicar realce de contraste
            smooth_kernel: Tamanho do kernel de suavização (None = sem suavização)
            
        Returns:
            Array processado
        """
        logger.info("Iniciando pipeline de processamento...")
        
        # Handle NaN values
        data = ImageProcessor.handle_nan(data)
        logger.info("NaN tratado")
        
        # Normaliza
        data = ImageProcessor.normalize(data, method=normalize_method)
        logger.info(f"Normalizado ({normalize_method})")
        
        # Aplica stretching
        if stretch_method == "asinh":
            data = ImageProcessor.asinh_stretch(data)
        elif stretch_method == "sqrt":
            data = ImageProcessor.sqrt_stretch(data)
        elif stretch_method == "log":
            data = ImageProcessor.log_stretch(data)
        logger.info(f"Stretching aplicado ({stretch_method})")
        
        # Realça contraste
        if enhance:
            data = ImageProcessor.enhance_contrast(data)
            logger.info("Contraste realçado")
        
        # Suaviza
        if smooth_kernel:
            data = ImageProcessor.smooth(data, kernel_size=smooth_kernel)
            logger.info(f"Suavização aplicada (kernel={smooth_kernel})")
        
        logger.info("Pipeline concluído!")
        return np.clip(data, 0, 1)
