"""
Módulo para leitura e análise de arquivos FITS (Flexible Image Transport System)
"""

import numpy as np
from astropy.io import fits
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FITSReader:
    """Leitor de arquivos FITS astronômicos"""
    
    def __init__(self, filepath: str):
        """
        Inicializa o leitor FITS
        
        Args:
            filepath: Caminho para o arquivo FITS
        """
        self.filepath = Path(filepath)
        self.hdul = None
        self.header = None
        self.data = None
        
    def load(self) -> bool:
        """
        Carrega o arquivo FITS
        
        Returns:
            bool: True se carregado com sucesso
        """
        try:
            if not self.filepath.exists():
                raise FileNotFoundError(f"Arquivo FITS não encontrado: {self.filepath}")
            
            self.hdul = fits.open(self.filepath)
            logger.info(f"Arquivo FITS carregado: {self.filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar FITS: {e}")
            return False
    
    def get_primary_data(self) -> Optional[np.ndarray]:
        """
        Extrai os dados da unidade primária
        
        Returns:
            Dados da imagem como array numpy
        """
        if self.hdul is None:
            self.load()
        
        return self.hdul[0].data if self.hdul else None
    
    def get_extension_data(self, extension: int = 1) -> Optional[np.ndarray]:
        """
        Extrai dados de uma extensão específica
        
        Args:
            extension: Número da extensão HDU
            
        Returns:
            Dados como array numpy
        """
        if self.hdul is None:
            self.load()
        
        if self.hdul and len(self.hdul) > extension:
            return self.hdul[extension].data
        return None
    
    def get_all_data(self) -> Dict[str, np.ndarray]:
        """
        Extrai todos os dados disponíveis
        
        Returns:
            Dicionário com todos os HDUs e seus dados
        """
        if self.hdul is None:
            self.load()
        
        data_dict = {}
        if self.hdul:
            for i, hdu in enumerate(self.hdul):
                if hdu.data is not None:
                    data_dict[f"hdu_{i}_{hdu.name}"] = hdu.data
        
        return data_dict
    
    def get_header(self, extension: int = 0) -> Optional[fits.Header]:
        """
        Obtém o header de uma extensão
        
        Args:
            extension: Número da extensão
            
        Returns:
            Header FITS
        """
        if self.hdul is None:
            self.load()
        
        if self.hdul and len(self.hdul) > extension:
            return self.hdul[extension].header
        return None
    
    def get_info(self) -> str:
        """
        Obtém informações sobre o arquivo FITS
        
        Returns:
            String com informações do arquivo
        """
        if self.hdul is None:
            self.load()
        
        if self.hdul:
            info = []
            info.append(f"Arquivo: {self.filepath.name}")
            info.append(f"Número de HDUs: {len(self.hdul)}")
            
            for i, hdu in enumerate(self.hdul):
                info.append(f"\nHDU {i}: {hdu.name if hdu.name else 'Primary'}")
                if hdu.data is not None:
                    info.append(f"  Shape: {hdu.data.shape}")
                    info.append(f"  Data type: {hdu.data.dtype}")
                    info.append(f"  Min: {np.nanmin(hdu.data):.2e}, Max: {np.nanmax(hdu.data):.2e}")
            
            return "\n".join(info)
        return "Arquivo não carregado"
    
    def close(self):
        """Fecha o arquivo FITS"""
        if self.hdul:
            self.hdul.close()
            self.hdul = None
    
    def __enter__(self):
        self.load()
        return self
    
    def __exit__(self, *args):
        self.close()


def load_fits(filepath: str) -> Optional[np.ndarray]:
    """
    Função helper para carregar rapidamente dados FITS
    
    Args:
        filepath: Caminho do arquivo FITS
        
    Returns:
        Array numpy com os dados
    """
    reader = FITSReader(filepath)
    if reader.load():
        data = reader.get_primary_data()
        reader.close()
        return data
    return None


def load_fits_multi_channel(filepath: str, channels: List[int] = None) -> Dict[str, np.ndarray]:
    """
    Carrega múltiplos canais de um arquivo FITS
    
    Args:
        filepath: Caminho do arquivo FITS
        channels: Lista de índices de extensões a carregar
        
    Returns:
        Dicionário com os canais
    """
    reader = FITSReader(filepath)
    if not reader.load():
        return {}
    
    data_dict = {}
    if channels is None:
        channels = range(len(reader.hdul))
    
    for channel in channels:
        data = reader.get_extension_data(channel) or reader.get_primary_data()
        if data is not None:
            data_dict[f"channel_{channel}"] = data
    
    reader.close()
    return data_dict
