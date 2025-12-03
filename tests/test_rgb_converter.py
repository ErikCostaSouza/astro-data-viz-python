"""
Testes unitários para o módulo rgb_converter
"""

import unittest
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rgb_converter import RGBConverter, create_rgb_image


class TestRGBConverter(unittest.TestCase):
    """Testes para RGBConverter"""
    
    def setUp(self):
        """Configura testes"""
        np.random.seed(42)
        self.channel_r = np.random.rand(100, 100)
        self.channel_g = np.random.rand(100, 100)
        self.channel_b = np.random.rand(100, 100)
    
    def test_combine_channels(self):
        """Testa combinação de canais"""
        result = RGBConverter.combine_channels(
            self.channel_r, self.channel_g, self.channel_b
        )
        
        self.assertEqual(result.shape, (100, 100, 3))
        self.assertGreaterEqual(result.min(), 0)
        self.assertLessEqual(result.max(), 1)
    
    def test_combine_channels_with_weights(self):
        """Testa combinação com pesos"""
        weights = (1.5, 1.0, 0.5)
        result = RGBConverter.combine_channels(
            self.channel_r, self.channel_g, self.channel_b,
            weights=weights
        )
        
        self.assertEqual(result.shape, (100, 100, 3))
    
    def test_colorize_monochrome(self):
        """Testa colorização monocromática"""
        result = RGBConverter.colorize_monochrome(self.channel_r, colormap="viridis")
        
        self.assertEqual(result.shape, (100, 100, 3))
        self.assertGreaterEqual(result.min(), 0)
        self.assertLessEqual(result.max(), 1)
    
    def test_colorize_different_colormaps(self):
        """Testa diferentes colormaps"""
        colormaps = ["hot", "cool", "plasma", "viridis"]
        
        for colormap in colormaps:
            result = RGBConverter.colorize_monochrome(self.channel_r, colormap)
            self.assertEqual(result.shape, (100, 100, 3))
    
    def test_create_from_single_channel(self):
        """Testa criação a partir de um único canal"""
        result = RGBConverter.create_from_single_channel(self.channel_r)
        
        self.assertEqual(result.shape, (100, 100, 3))
    
    def test_blend_channels(self):
        """Testa mistura de canais"""
        result = RGBConverter.blend_channels(self.channel_r, self.channel_g, alpha=0.5)
        
        self.assertEqual(result.shape, self.channel_r.shape)
    
    def test_equalize_channels(self):
        """Testa equalização de canais"""
        r, g, b = RGBConverter.equalize_channels(
            self.channel_r, self.channel_g, self.channel_b
        )
        
        self.assertEqual(r.shape, self.channel_r.shape)
        self.assertEqual(g.shape, self.channel_g.shape)
        self.assertEqual(b.shape, self.channel_b.shape)
    
    def test_map_filters_to_rgb(self):
        """Testa mapeamento de filtros"""
        filters = {
            'red': self.channel_r,
            'green': self.channel_g,
            'blue': self.channel_b
        }
        
        mapping = {
            'red': 'red',
            'green': 'green',
            'blue': 'blue'
        }
        
        result = RGBConverter.map_filters_to_rgb(filters, mapping)
        self.assertEqual(result.shape, (100, 100, 3))


class TestCreateRgbImage(unittest.TestCase):
    """Testes para função helper create_rgb_image"""
    
    def setUp(self):
        np.random.seed(42)
        self.channels = [
            np.random.rand(100, 100),
            np.random.rand(100, 100),
            np.random.rand(100, 100)
        ]
    
    def test_create_rgb_image(self):
        """Testa criação de imagem RGB"""
        result = create_rgb_image(self.channels)
        self.assertEqual(result.shape, (100, 100, 3))
    
    def test_create_rgb_image_insufficient_channels(self):
        """Testa erro com canais insuficientes"""
        with self.assertRaises(ValueError):
            create_rgb_image([self.channels[0]])


if __name__ == "__main__":
    unittest.main()
