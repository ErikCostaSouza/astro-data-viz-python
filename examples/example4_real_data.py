"""
Exemplo 4: Processar Dados Reais do MAST
Demonstra como baixar dados de telescópios reais e processar com o pipeline
"""

import sys
from pathlib import Path

# Adiciona src ao path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from fits_reader import FITSReader
from image_processor import ImageProcessor
from rgb_converter import RGBConverter
from pipeline import AstroDataVizPipeline


def example_process_mast_data():
    """
    Processa dados baixados do MAST
    
    Antes de rodar:
    1. python download_mast_data.py --target "M51" --limit 1
    
    Isso irá criar arquivo em ./data/raw/hubble_M51_1.fits
    """
    
    print("\n" + "="*60)
    print("🌌 EXEMPLO 4: Processamento de Dados Reais (MAST)")
    print("="*60)
    
    # Arquivo FITS baixado do MAST
    fits_file = "./data/raw/hubble_M51_1.fits"
    
    # Verifica se arquivo existe
    if not Path(fits_file).exists():
        print(f"\n❌ Arquivo não encontrado: {fits_file}")
        print("\n💡 Para baixar dados reais do MAST, execute:")
        print("   python download_mast_data.py --target M51 --process")
        print("\nOu use dados sintéticos:")
        print("   fits_file = './data/raw/synthetic_multiband.fits'")
        return
    
    print(f"\n📁 Processando: {fits_file}")
    
    # ==========================================
    # PASSO 1: Inspecionar Arquivo FITS
    # ==========================================
    print("\n[PASSO 1] 📋 Inspecionando arquivo FITS...")
    
    try:
        with FITSReader(fits_file) as reader:
            print(reader.get_info())
            data = reader.get_primary_data()
            
            if data is not None:
                print(f"\n📊 Estatísticas:")
                print(f"   Shape: {data.shape}")
                print(f"   Tipo: {data.dtype}")
                print(f"   Min: {data.min():.2e}")
                print(f"   Max: {data.max():.2e}")
                print(f"   Média: {data.mean():.2e}")
                print(f"   NaN: {(data != data).sum()} pixels")
    
    except Exception as e:
        print(f"❌ Erro ao inspecionar: {e}")
        return
    
    # ==========================================
    # PASSO 2: Aplicar Pipeline de Processamento
    # ==========================================
    print("\n[PASSO 2] 🔄 Aplicando pipeline de processamento...")
    
    try:
        # Diferentes configurações de processamento
        configs = [
            {
                "name": "Padrão (Asinh + Hot)",
                "params": {
                    "normalize_method": "percentile",
                    "stretch_method": "asinh",
                    "enhance": True,
                    "smooth_kernel": 3
                },
                "colormap": "hot"
            },
            {
                "name": "Contraste Alto (Log + Viridis)",
                "params": {
                    "normalize_method": "minmax",
                    "stretch_method": "log",
                    "enhance": True,
                    "smooth_kernel": 5
                },
                "colormap": "viridis"
            },
            {
                "name": "Suave (Sqrt + Cool)",
                "params": {
                    "normalize_method": "zscore",
                    "stretch_method": "sqrt",
                    "enhance": False,
                    "smooth_kernel": 1
                },
                "colormap": "cool"
            }
        ]
        
        results = []
        
        for i, config in enumerate(configs, 1):
            print(f"\n   Configuração {i}: {config['name']}")
            
            # Carrega dados
            with FITSReader(fits_file) as reader:
                data = reader.get_primary_data()
            
            if data is None:
                print("   ❌ Não conseguiu carregar dados")
                continue
            
            # Processa
            processed = ImageProcessor.apply_pipeline(
                data,
                **config["params"]
            )
            
            # Coloriza
            rgb = RGBConverter.colorize_monochrome(
                processed,
                config["colormap"]
            )
            
            print(f"   ✅ RGB shape: {rgb.shape}")
            print(f"   ✅ Range: [{rgb.min():.3f}, {rgb.max():.3f}]")
            
            results.append({
                "name": config["name"],
                "rgb": rgb,
                "config": config
            })
        
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # ==========================================
    # PASSO 3: Salvar Resultados
    # ==========================================
    print("\n[PASSO 3] 💾 Salvando resultados...")
    
    try:
        pipeline = AstroDataVizPipeline("./data/processed")
        
        base_name = Path(fits_file).stem
        
        for i, result in enumerate(results, 1):
            output_name = f"{base_name}_config{i}_{result['name'].replace(' ', '_').lower()}.png"
            output_path = f"./data/processed/{output_name}"
            
            pipeline._save_rgb_image(result["rgb"], output_path)
            print(f"   ✅ {output_name}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return
    
    # ==========================================
    # PASSO 4: Resumo
    # ==========================================
    print("\n" + "="*60)
    print("✅ PROCESSAMENTO CONCLUÍDO")
    print("="*60)
    
    print(f"\n📊 Resumo:")
    print(f"   Arquivo original: {fits_file}")
    print(f"   Imagens processadas: {len(results)}")
    print(f"   Salvas em: ./data/processed/")
    
    print(f"\n🎨 Configurações aplicadas:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['name']}")
        print(f"      Normalização: {result['config']['params']['normalize_method']}")
        print(f"      Stretching: {result['config']['params']['stretch_method']}")
        print(f"      Colormap: {result['config']['colormap']}")
    
    print(f"\n💡 Próximos passos:")
    print(f"   1. Visualize os arquivos PNG em ./data/processed/")
    print(f"   2. Compare diferentes configurações")
    print(f"   3. Ajuste parâmetros conforme necessário")
    print(f"   4. Baixe mais dados: python download_mast_data.py --target NGC6543")
    
    print("\n" + "="*60)


def example_multi_band_real_data():
    """
    Exemplo de processamento multi-banda com dados reais
    (Simulado com dados sintéticos, mas válido para dados reais)
    """
    
    print("\n" + "="*60)
    print("🌌 EXEMPLO 4B: Multi-Banda (Hubble Palette)")
    print("="*60)
    
    fits_file = "./data/raw/synthetic_multiband.fits"
    
    if not Path(fits_file).exists():
        print(f"\n❌ Arquivo não encontrado: {fits_file}")
        return
    
    print(f"\n📁 Processando arquivo multi-banda: {fits_file}")
    
    try:
        # Carrega todas as extensões
        with FITSReader(fits_file) as reader:
            all_data = reader.get_all_data()
        
        print(f"✅ {len(all_data)} bandas carregadas")
        
        # Processa os primeiros 3 canais
        channels = []
        
        for i, (name, data) in enumerate(list(all_data.items())[:3]):
            print(f"\n   Processando banda {i+1}: {name}")
            
            processed = ImageProcessor.apply_pipeline(
                data,
                normalize_method="percentile",
                stretch_method="asinh",
                enhance=True,
                smooth_kernel=3
            )
            
            channels.append(processed)
            print(f"   ✅ Shape: {processed.shape}")
        
        # Combina em RGB
        rgb = RGBConverter.combine_channels(
            channels[0], channels[1], channels[2]
        )
        
        print(f"\n✅ RGB criado: {rgb.shape}")
        
        # Salva
        pipeline = AstroDataVizPipeline("./data/processed")
        pipeline._save_rgb_image(
            rgb,
            "./data/processed/multiband_rgb_hubble_palette.png"
        )
        
        print(f"✅ Salvo: multiband_rgb_hubble_palette.png")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🚀 Exemplos de Processamento de Dados Reais")
    print("\n💡 IMPORTANTE: Antes de rodar, baixe dados do MAST com:")
    print("   python download_mast_data.py --target M51 --process")
    
    # Tenta exemplo principal
    example_process_mast_data()
    
    # Tenta exemplo multi-banda
    example_multi_band_real_data()
    
    print("\n✨ Exemplos completados!")
