"""
Visualizador interativo de metadados FITS
Mostra informações de telescópios, filtros, datas, etc
"""

import sys
from pathlib import Path
import argparse

# Adiciona src ao path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from fits_reader import FITSReader


def show_telescope_info(header):
    """Extrai informações do telescópio do header"""
    print("\n🔭 INFORMAÇÕES DO TELESCÓPIO")
    print("=" * 60)
    
    telescopes = {
        'TELESCOP': 'Telescópio',
        'INSTRUME': 'Instrumento',
        'DETECTOR': 'Detector',
        'FILTER': 'Filtro',
        'FILTER1': 'Filtro 1',
        'FILTER2': 'Filtro 2',
        'EXPTIME': 'Tempo de Exposição (s)',
        'EXPSTART': 'Início da Exposição',
        'EXPEND': 'Fim da Exposição',
        'DATE-OBS': 'Data de Observação',
        'TIME-OBS': 'Hora de Observação',
        'RA_TARG': 'Ascensão Reta',
        'DEC_TARG': 'Declinação',
        'PROPOSID': 'ID da Proposta',
        'TARGNAME': 'Nome do Alvo',
    }
    
    for key, description in telescopes.items():
        if key in header:
            value = header[key]
            print(f"  {description:.<40} {value}")


def show_data_info(header):
    """Informações sobre os dados"""
    print("\n📊 INFORMAÇÕES DOS DADOS")
    print("=" * 60)
    
    data_keys = {
        'NAXIS1': 'Largura (pixels)',
        'NAXIS2': 'Altura (pixels)',
        'NAXIS3': 'Profundidade (pixels)',
        'BITPIX': 'Bits por pixel',
        'BSCALE': 'Escala de Byte',
        'BZERO': 'Zero de Byte',
        'DATAMIN': 'Valor Mínimo',
        'DATAMAX': 'Valor Máximo',
        'EXTNAME': 'Nome da Extensão',
        'EXTVER': 'Versão da Extensão',
    }
    
    for key, description in data_keys.items():
        if key in header:
            value = header[key]
            print(f"  {description:.<40} {value}")


def show_calibration_info(header):
    """Informações de calibração"""
    print("\n🔧 INFORMAÇÕES DE CALIBRAÇÃO")
    print("=" * 60)
    
    calibration_keys = {
        'WAVELNTH': 'Comprimento de Onda',
        'APERTURE': 'Abertura',
        'GAIN': 'Ganho',
        'READNOISE': 'Ruído de Leitura',
        'FLATFILE': 'Arquivo Flat',
        'DARKFILE': 'Arquivo Dark',
        'BIASFILE': 'Arquivo Bias',
        'CCDTEMP': 'Temperatura do CCD',
    }
    
    found = False
    for key, description in calibration_keys.items():
        if key in header:
            found = True
            value = header[key]
            print(f"  {description:.<40} {value}")
    
    if not found:
        print("  (Nenhuma informação de calibração disponível)")


def show_wcs_info(header):
    """Informações de calibração de coordenadas"""
    print("\n📍 INFORMAÇÕES WCS (Coordenadas)")
    print("=" * 60)
    
    wcs_keys = {
        'CRVAL1': 'Valor de Referência RA',
        'CRVAL2': 'Valor de Referência Dec',
        'CRPIX1': 'Pixel de Referência X',
        'CRPIX2': 'Pixel de Referência Y',
        'CD1_1': 'CD Matrix (1,1)',
        'CD1_2': 'CD Matrix (1,2)',
        'CD2_1': 'CD Matrix (2,1)',
        'CD2_2': 'CD Matrix (2,2)',
        'CTYPE1': 'Tipo de Coordenada 1',
        'CTYPE2': 'Tipo de Coordenada 2',
        'CUNIT1': 'Unidade Coordenada 1',
        'CUNIT2': 'Unidade Coordenada 2',
    }
    
    found = False
    for key, description in wcs_keys.items():
        if key in header:
            found = True
            value = header[key]
            if isinstance(value, float):
                print(f"  {description:.<40} {value:.6f}")
            else:
                print(f"  {description:.<40} {value}")
    
    if not found:
        print("  (Nenhuma informação WCS disponível)")


def show_processing_info(header):
    """Histórico de processamento"""
    print("\n⚙️ HISTÓRICO DE PROCESSAMENTO")
    print("=" * 60)
    
    processing_keys = {
        'ORIGFILE': 'Arquivo Original',
        'PROCVER': 'Versão de Processamento',
        'PRODNAME': 'Nome do Produto',
        'CALVER': 'Versão de Calibração',
    }
    
    found = False
    for key, description in processing_keys.items():
        if key in header:
            found = True
            value = header[key]
            print(f"  {description:.<40} {value}")
    
    # Procura por HISTORY
    if 'HISTORY' in header:
        found = True
        print(f"\n  Histórico:")
        histories = header['HISTORY']
        if isinstance(histories, list):
            for history in histories[:5]:  # Primeiras 5
                print(f"    • {history}")
        else:
            print(f"    • {histories}")


def show_custom_comments(header):
    """Mostra comentários customizados"""
    print("\n💬 COMENTÁRIOS IMPORTANTES")
    print("=" * 60)
    
    important_keywords = {
        'ORIGIN': 'Origem',
        'OBJECT': 'Objeto',
        'OBSERVER': 'Observador',
        'PROGRAM': 'Programa',
        'OBSERVAT': 'Observatório',
        'PI_NAME': 'PI (Principal Investigator)',
        'AUTHOR': 'Autor',
        'DESCRIP': 'Descrição',
    }
    
    found = False
    for key, description in important_keywords.items():
        if key in header:
            found = True
            value = header[key]
            print(f"  {description:.<40} {value}")
    
    if not found:
        print("  (Nenhum comentário importante encontrado)")


def visualize_fits(filepath: str, verbose: bool = False):
    """
    Visualiza todas as informações de um arquivo FITS
    
    Args:
        filepath: Caminho do arquivo FITS
        verbose: Mostrar todos os headers
    """
    
    path = Path(filepath)
    
    if not path.exists():
        print(f"❌ Arquivo não encontrado: {filepath}")
        return
    
    print("\n" + "=" * 60)
    print("📁 VISUALIZADOR DE METADADOS FITS")
    print("=" * 60)
    
    print(f"\n📂 Arquivo: {path.name}")
    print(f"   Tamanho: {path.stat().st_size / (1024*1024):.2f} MB")
    print(f"   Caminho: {path.absolute()}")
    
    try:
        with FITSReader(filepath) as reader:
            # Informações gerais
            info = reader.get_info()
            print(f"\n{info}")
            
            # Headers
            header = reader.get_header()
            
            if header:
                show_telescope_info(header)
                show_data_info(header)
                show_calibration_info(header)
                show_wcs_info(header)
                show_processing_info(header)
                show_custom_comments(header)
                
                if verbose:
                    print("\n📋 TODOS OS HEADERS (Verbose)")
                    print("=" * 60)
                    for key, value in header.items():
                        if key not in ['HISTORY', 'COMMENT']:
                            print(f"  {key:.<20} {value}")
            
            # Dados
            data = reader.get_primary_data()
            if data is not None:
                print("\n🔢 ESTATÍSTICAS DOS DADOS")
                print("=" * 60)
                print(f"  Shape: {data.shape}")
                print(f"  Tipo: {data.dtype}")
                print(f"  Min: {data.min():.2e}")
                print(f"  Max: {data.max():.2e}")
                print(f"  Média: {data.mean():.2e}")
                print(f"  Desvio Padrão: {data.std():.2e}")
                print(f"  NaN: {(data != data).sum()} pixels")
                print(f"  Inf: {(data == float('inf')).sum()} pixels")
            
            # Extensões
            all_data = reader.get_all_data()
            if len(all_data) > 1:
                print(f"\n📦 EXTENSÕES ({len(all_data)} total)")
                print("=" * 60)
                for i, (name, data) in enumerate(all_data.items(), 1):
                    print(f"  {i}. {name:.<30} {data.shape}")
    
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Visualiza metadados FITS de telescópios"
    )
    
    parser.add_argument(
        "fits_file",
        nargs="?",
        default=None,
        help="Arquivo FITS a visualizar"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra todos os headers"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Lista arquivos FITS em data/raw"
    )
    
    args = parser.parse_args()
    
    if args.list or args.fits_file is None:
        print("\n📁 Arquivos FITS em ./data/raw/:")
        fits_dir = Path("./data/raw")
        if fits_dir.exists():
            for fits_file in sorted(fits_dir.glob("*.fits")):
                size_mb = fits_file.stat().st_size / (1024*1024)
                print(f"  • {fits_file.name:.<40} {size_mb:>8.2f} MB")
        else:
            print("  (Diretório não encontrado)")
        return
    
    visualize_fits(args.fits_file, verbose=args.verbose)


if __name__ == "__main__":
    main()
