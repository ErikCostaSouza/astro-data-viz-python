#!/usr/bin/env python
"""
Setup e script de demonstração rápida do projeto Astro Data Visualization
"""

import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Verifica versão mínima do Python"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ requerido!")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def install_dependencies():
    """Instala as dependências do projeto"""
    print("\n📦 Instalando dependências...")
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando estrutura de diretórios...")
    dirs = [
        "data/raw",
        "data/processed",
        "notebooks",
        "tests"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Diretórios criados/verificados!")

def run_demo():
    """Executa uma demonstração rápida"""
    print("\n🚀 Executando demonstração...")
    
    demo_script = Path(__file__).parent / "examples" / "example1_basic.py"
    
    try:
        subprocess.run([sys.executable, str(demo_script)], check=True)
        print("\n✅ Demonstração concluída!")
    except subprocess.CalledProcessError:
        print("\n❌ Erro ao executar demonstração")

def print_menu():
    """Imprime menu de opções"""
    print("\n" + "="*60)
    print("🌌 Astro Data Visualization - Setup & Demo")
    print("="*60)
    print("\nOpções:")
    print("1. Instalação completa (dependências + diretórios + demo)")
    print("2. Apenas instalar dependências")
    print("3. Apenas criar diretórios")
    print("4. Apenas executar demo")
    print("5. Mostrar informações")
    print("0. Sair")
    print("-"*60)

def show_info():
    """Mostra informações do projeto"""
    print("""
🌌 ASTRO DATA VISUALIZATION

Um pipeline completo em Python para transformar dados brutos FITS 
de telescópios espaciais em imagens RGB coloridas.

📊 Funcionalidades:
   • Leitura de arquivos FITS (Hubble, JWST)
   • Processamento avançado de imagens
   • Normalização e stretching
   • Conversão para RGB com múltiplas paletas
   • Gerador de dados FITS sintéticos
   • Testes unitários completos

📚 Exemplos:
   • example1_basic.py: Uso básico
   • example2_colorization.py: Múltiplos colormaps
   • example3_advanced.py: Técnicas avançadas

🔗 Documentação:
   Veja README_PROJETO.md para guia completo

✨ Versão: 1.0.0
👤 Autor: Erik Costa Souza
    """)

def main():
    """Menu principal"""
    check_python_version()
    
    while True:
        print_menu()
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            install_dependencies()
            create_directories()
            run_demo()
        elif choice == "2":
            install_dependencies()
        elif choice == "3":
            create_directories()
        elif choice == "4":
            run_demo()
        elif choice == "5":
            show_info()
        elif choice == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
        sys.exit(0)
