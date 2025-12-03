"""
Testes unitários para o módulo image_processor
"""

import unittest
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    """Testes para ImageProcessor"""
    
    def setUp(self):
        """Configura testes"""
        np.random.seed(42)
        self.test_image = np.random.rand(100, 100) * 1000
        self.normalized_image = np.random.rand(100, 100)
    
    def test_normalize_minmax(self):
        """Testa normalização minmax"""
        result = ImageProcessor.normalize(self.test_image, method="minmax")
        self.assertGreaterEqual(result.min(), 0)
        self.assertLessEqual(result.max(), 1)
    
    def test_normalize_percentile(self):
        """Testa normalização por percentil"""
        result = ImageProcessor.normalize(self.test_image, method="percentile")
        self.assertGreaterEqual(result.min(), -0.5)
        self.assertLessEqual(result.max(), 1.5)
    
    def test_normalize_zscore(self):
        """Testa normalização z-score"""
        result = ImageProcessor.normalize(self.test_image, method="zscore")
        self.assertGreater(result.mean(), -1)
        self.assertLess(result.mean(), 1)
    
    def test_asinh_stretch(self):
        """Testa stretching asinh"""
        result = ImageProcessor.asinh_stretch(self.normalized_image)
        self.assertGreaterEqual(result.min(), 0)
        self.assertLessEqual(result.max(), 1)
    
    def test_sqrt_stretch(self):
        """Testa stretching raiz quadrada"""
        result = ImageProcessor.sqrt_stretch(self.normalized_image)
        self.assertGreaterEqual(result.min(), 0)
        self.assertLessEqual(result.max(), 1)
    
    def test_log_stretch(self):
        """Testa stretching logarítmico"""
        result = ImageProcessor.log_stretch(self.normalized_image)
        self.assertGreaterEqual(result.min(), 0)
        self.assertLessEqual(result.max(), 1)
    
    def test_enhance_contrast(self):
        """Testa aumento de contraste"""
        result = ImageProcessor.enhance_contrast(self.normalized_image)
        self.assertEqual(result.shape, self.normalized_image.shape)
        self.assertGreaterEqual(result.min(), 0)
    
    def test_smooth(self):
        """Testa suavização"""
        result = ImageProcessor.smooth(self.test_image, kernel_size=3)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_sharpen(self):
        """Testa aguçamento"""
        result = ImageProcessor.sharpen(self.normalized_image, amount=0.5)
        self.assertEqual(result.shape, self.normalized_image.shape)
    
    def test_handle_nan_zero(self):
        """Testa tratamento de NaN com zero"""
        data = self.test_image.astype(float)
        data[10:15, 10:15] = np.nan
        result = ImageProcessor.handle_nan(data, method="zero")
        self.assertFalse(np.any(np.isnan(result)))
        self.assertEqual(result[10, 10], 0)
    
    def test_handle_nan_mean(self):
        """Testa tratamento de NaN com média"""
        data = self.test_image.astype(float)
        data[10:15, 10:15] = np.nan
        result = ImageProcessor.handle_nan(data, method="mean")
        self.assertFalse(np.any(np.isnan(result)))
    
    def test_apply_pipeline(self):
        """Testa pipeline completo"""
        result = ImageProcessor.apply_pipeline(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
        self.assertGreaterEqual(result.min(), 0)
        self.assertLessEqual(result.max(), 1)


if __name__ == "__main__":
    unittest.main()
