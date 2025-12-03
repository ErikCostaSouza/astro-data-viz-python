"""
Testes unitários para o módulo fits_reader
"""

import unittest
import numpy as np
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fits_reader import FITSReader, load_fits
from synthetic_fits_generator import create_monochrome_fits, create_multiband_fits


class TestFITSReader(unittest.TestCase):
    """Testes para FITSReader"""
    
    def setUp(self):
        """Configura testes"""
        self.temp_dir = tempfile.mkdtemp()
        self.mono_path = Path(self.temp_dir) / "test_mono.fits"
        self.multi_path = Path(self.temp_dir) / "test_multi.fits"
        
        create_monochrome_fits(str(self.mono_path))
        create_multiband_fits(str(self.multi_path), n_bands=3)
    
    def test_load_monochrome(self):
        """Testa carregamento de FITS monocromático"""
        reader = FITSReader(str(self.mono_path))
        self.assertTrue(reader.load())
        data = reader.get_primary_data()
        self.assertIsNotNone(data)
        self.assertEqual(len(data.shape), 2)
        reader.close()
    
    def test_load_multiband(self):
        """Testa carregamento de FITS multi-banda"""
        reader = FITSReader(str(self.multi_path))
        self.assertTrue(reader.load())
        
        all_data = reader.get_all_data()
        self.assertGreater(len(all_data), 1)
        
        reader.close()
    
    def test_context_manager(self):
        """Testa uso como context manager"""
        with FITSReader(str(self.mono_path)) as reader:
            data = reader.get_primary_data()
            self.assertIsNotNone(data)
    
    def test_get_header(self):
        """Testa extração de header"""
        with FITSReader(str(self.mono_path)) as reader:
            header = reader.get_header()
            self.assertIsNotNone(header)
    
    def test_load_nonexistent_file(self):
        """Testa carregamento de arquivo inexistente"""
        reader = FITSReader("/nonexistent/file.fits")
        self.assertFalse(reader.load())


class TestLoad_fits_helper(unittest.TestCase):
    """Testes para função helper load_fits"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fits_path = Path(self.temp_dir) / "test.fits"
        create_monochrome_fits(str(self.fits_path))
    
    def test_load_fits_helper(self):
        """Testa função helper load_fits"""
        data = load_fits(str(self.fits_path))
        self.assertIsNotNone(data)
        self.assertEqual(len(data.shape), 2)


if __name__ == "__main__":
    unittest.main()
