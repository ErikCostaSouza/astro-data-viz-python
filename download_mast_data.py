"""
Script para baixar dados reais do MAST (Barbara A. Mikulski Archive)
Suporta Hubble, JWST e outros telescópios
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def install_astroquery():
    """Instala astroquery se não estiver disponível"""
    try:
        import astroquery
        logger.info("✅ astroquery já instalado")
    except ImportError:
        logger.warning("❌ astroquery não encontrado. Instalando...")
        os.system("pip install astroquery --quiet")
        logger.info("✅ astroquery instalado")


def download_hubble_data(target: str = "M51", 
                        output_dir: str = "./data/raw",
                        limit: int = 5) -> List[str]:
    """
    Baixa imagens do Hubble Space Telescope
    
    Args:
        target: Nome do objeto (M51, NGC6543, M31, etc)
        output_dir: Diretório de saída
        limit: Número máximo de arquivos
        
    Returns:
        Lista de arquivos baixados
    """
    try:
        from astroquery.mast import Observations
        import time
    except ImportError:
        logger.error("astroquery não disponível. Instale com: pip install astroquery")
        return []
    
    logger.info(f"\n🔍 Procurando por imagens do Hubble: {target}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Busca observações
        obs_table = Observations.query_object(target, radius=0.1)
        
        if len(obs_table) == 0:
            logger.warning(f"❌ Nenhuma observação encontrada para {target}")
            return []
        
        logger.info(f"✅ Encontradas {len(obs_table)} observações")
        
        # Filtra apenas Hubble
        hubble_obs = obs_table[obs_table['obs_collection'] == 'HST']
        
        if len(hubble_obs) == 0:
            logger.warning("❌ Nenhuma observação do Hubble encontrada")
            logger.info("💡 Dica: Tente outros alvos como 'NGC 6543', 'Hubble Deep Field'")
            return []
        
        logger.info(f"✅ {len(hubble_obs)} observações do Hubble disponíveis")
        
        # Pega os primeiros N
        hubble_obs = hubble_obs[:limit]
        
        downloaded_files = []
        
        for i, obs in enumerate(hubble_obs, 1):
            try:
                logger.info(f"\n📥 Baixando observação {i}/{min(len(hubble_obs), limit)}...")
                logger.info(f"   Data: {obs['obs_id']}")
                logger.info(f"   Instrumento: {obs['instrument_name']}")
                
                # Baixa os dados
                products = Observations.get_product_list(obs)
                
                if len(products) == 0:
                    logger.warning("   ⚠️ Nenhum arquivo disponível")
                    continue
                
                # Filtra apenas FITS
                fits_products = products[products['productFilename'].str.endswith('.fits')]
                
                if len(fits_products) == 0:
                    logger.warning("   ⚠️ Nenhum arquivo FITS encontrado")
                    continue
                
                # Baixa apenas o primeiro FITS de cada observação
                product = fits_products[0]
                
                output_file = os.path.join(
                    output_dir, 
                    f"hubble_{target.replace(' ', '_')}_{i}.fits"
                )
                
                # Evita re-download
                if os.path.exists(output_file):
                    logger.info(f"   ✅ Já existe: {os.path.basename(output_file)}")
                    downloaded_files.append(output_file)
                    continue
                
                # Download via MAST
                manifest = Observations.download_products(
                    obs,
                    productFilename=product['productFilename'],
                    download_dir=output_dir
                )
                
                if len(manifest) > 0:
                    downloaded_file = manifest['Local Path'][0]
                    # Renomeia para ficar mais organizado
                    new_name = os.path.join(
                        output_dir,
                        f"hubble_{target.replace(' ', '_')}_{i}.fits"
                    )
                    
                    # Move arquivo original
                    if os.path.exists(downloaded_file):
                        import shutil
                        shutil.move(downloaded_file, new_name)
                        logger.info(f"   ✅ Salvo: {os.path.basename(new_name)}")
                        downloaded_files.append(new_name)
                
                # Evita rate limit
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"   ⚠️ Erro ao baixar: {e}")
                continue
        
        if downloaded_files:
            logger.info(f"\n✅ Total baixado: {len(downloaded_files)} arquivo(s)")
        else:
            logger.warning("\n❌ Nenhum arquivo foi baixado com sucesso")
        
        return downloaded_files
        
    except Exception as e:
        logger.error(f"Erro ao buscar dados do Hubble: {e}")
        return []


def download_jwst_data(target: str = "CEERS",
                      output_dir: str = "./data/raw",
                      limit: int = 3) -> List[str]:
    """
    Baixa imagens do James Webb Space Telescope
    
    Args:
        target: Nome do programa ou alvo
        output_dir: Diretório de saída
        limit: Número máximo de arquivos
        
    Returns:
        Lista de arquivos baixados
    """
    try:
        from astroquery.mast import Observations
        import time
    except ImportError:
        logger.error("astroquery não disponível. Instale com: pip install astroquery")
        return []
    
    logger.info(f"\n🔍 Procurando por imagens do JWST: {target}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Busca observações JWST
        obs_table = Observations.query_criteria(
            obs_collection=['JWST'],
            target_name=target,
            intentType='science'
        )
        
        if len(obs_table) == 0:
            logger.warning(f"❌ Nenhuma observação JWST encontrada para {target}")
            logger.info("💡 Tente: 'GN-COSMOS', 'GS-COSMOS', 'ERGs', 'CANDELS'")
            return []
        
        logger.info(f"✅ Encontradas {len(obs_table)} observações JWST")
        
        obs_table = obs_table[:limit]
        
        downloaded_files = []
        
        for i, obs in enumerate(obs_table, 1):
            try:
                logger.info(f"\n📥 Baixando observação JWST {i}/{min(len(obs_table), limit)}...")
                logger.info(f"   Data: {obs['obs_id']}")
                logger.info(f"   Instrumento: {obs['instrument_name']}")
                
                products = Observations.get_product_list(obs)
                
                if len(products) == 0:
                    logger.warning("   ⚠️ Nenhum arquivo disponível")
                    continue
                
                # Filtra apenas FITS
                fits_products = products[products['productFilename'].str.endswith('.fits')]
                
                if len(fits_products) == 0:
                    logger.warning("   ⚠️ Nenhum arquivo FITS encontrado")
                    continue
                
                product = fits_products[0]
                
                output_file = os.path.join(
                    output_dir,
                    f"jwst_{target.replace(' ', '_')}_{i}.fits"
                )
                
                if os.path.exists(output_file):
                    logger.info(f"   ✅ Já existe: {os.path.basename(output_file)}")
                    downloaded_files.append(output_file)
                    continue
                
                manifest = Observations.download_products(
                    obs,
                    productFilename=product['productFilename'],
                    download_dir=output_dir
                )
                
                if len(manifest) > 0:
                    downloaded_file = manifest['Local Path'][0]
                    new_name = os.path.join(
                        output_dir,
                        f"jwst_{target.replace(' ', '_')}_{i}.fits"
                    )
                    
                    if os.path.exists(downloaded_file):
                        import shutil
                        shutil.move(downloaded_file, new_name)
                        logger.info(f"   ✅ Salvo: {os.path.basename(new_name)}")
                        downloaded_files.append(new_name)
                
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"   ⚠️ Erro ao baixar: {e}")
                continue
        
        if downloaded_files:
            logger.info(f"\n✅ Total baixado: {len(downloaded_files)} arquivo(s)")
        else:
            logger.warning("\n❌ Nenhum arquivo foi baixado com sucesso")
        
        return downloaded_files
        
    except Exception as e:
        logger.error(f"Erro ao buscar dados do JWST: {e}")
        return []


def inspect_fits_file(filepath: str):
    """Inspeciona um arquivo FITS baixado"""
    try:
        from fits_reader import FITSReader
    except ImportError:
        logger.error("Adicione './src' ao path para usar FITSReader")
        return
    
    logger.info(f"\n📋 Inspecionando: {os.path.basename(filepath)}")
    
    try:
        with FITSReader(filepath) as reader:
            print(reader.get_info())
            
            data = reader.get_primary_data()
            if data is not None:
                print(f"\n📊 Dados principais:")
                print(f"   Shape: {data.shape}")
                print(f"   Tipo: {data.dtype}")
                print(f"   Min: {data.min():.2e}")
                print(f"   Max: {data.max():.2e}")
                
    except Exception as e:
        logger.error(f"Erro ao inspecionar: {e}")


def process_downloaded_data(filepath: str, output_dir: str = "./data/processed"):
    """Processa arquivo FITS baixado usando o pipeline"""
    try:
        sys.path.insert(0, './src')
        from fits_reader import FITSReader
        from image_processor import ImageProcessor
        from rgb_converter import RGBConverter
    except ImportError as e:
        logger.error(f"Erro ao importar módulos do pipeline: {e}")
        return None
    
    logger.info(f"\n🔄 Processando: {os.path.basename(filepath)}")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with FITSReader(filepath) as reader:
            data = reader.get_primary_data()
        
        if data is None:
            logger.error("❌ Não conseguiu carregar dados FITS")
            return None
        
        logger.info("✅ Dados carregados")
        
        # Processa
        logger.info("🔄 Normalizando...")
        processed = ImageProcessor.apply_pipeline(
            data,
            normalize_method="percentile",
            stretch_method="asinh",
            enhance=True,
            smooth_kernel=3
        )
        
        logger.info("🎨 Colorindo...")
        rgb = RGBConverter.colorize_monochrome(processed, "hot")
        
        # Salva
        from pipeline import AstroDataVizPipeline
        pipeline = AstroDataVizPipeline(output_dir)
        
        base_name = Path(filepath).stem
        output_path = os.path.join(output_dir, f"{base_name}_processed.png")
        
        pipeline._save_rgb_image(rgb, output_path)
        
        logger.info(f"✅ Processado: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Menu principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Baixa dados reais do MAST (Hubble, JWST, etc)"
    )
    
    parser.add_argument(
        "--source",
        choices=["hubble", "jwst", "both"],
        default="hubble",
        help="Fonte de dados"
    )
    
    parser.add_argument(
        "--target",
        default=None,
        help="Alvo a buscar (ex: M51, NGC6543 para Hubble; CEERS para JWST)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Número máximo de arquivos a baixar"
    )
    
    parser.add_argument(
        "--output",
        default="./data/raw",
        help="Diretório de saída"
    )
    
    parser.add_argument(
        "--process",
        action="store_true",
        help="Processa os arquivos baixados com o pipeline"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("📡 MAST DATA DOWNLOADER")
    logger.info("=" * 60)
    
    # Garante que astroquery está instalado
    install_astroquery()
    
    downloaded_files = []
    
    if args.source in ["hubble", "both"]:
        target = args.target or "M51"
        hubble_files = download_hubble_data(
            target=target,
            output_dir=args.output,
            limit=args.limit
        )
        downloaded_files.extend(hubble_files)
    
    if args.source in ["jwst", "both"]:
        target = args.target or "CEERS"
        jwst_files = download_jwst_data(
            target=target,
            output_dir=args.output,
            limit=args.limit
        )
        downloaded_files.extend(jwst_files)
    
    # Inspeciona arquivos
    if downloaded_files:
        logger.info("\n" + "=" * 60)
        logger.info("📋 INSPEÇÃO DOS ARQUIVOS BAIXADOS")
        logger.info("=" * 60)
        
        for filepath in downloaded_files[:3]:  # Inspeciona apenas 3 primeiros
            inspect_fits_file(filepath)
        
        # Processa se solicitado
        if args.process:
            logger.info("\n" + "=" * 60)
            logger.info("🔄 PROCESSAMENTO COM PIPELINE")
            logger.info("=" * 60)
            
            for filepath in downloaded_files:
                process_downloaded_data(filepath)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ CONCLUÍDO")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
