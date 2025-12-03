@echo off
REM Script de setup para Windows

echo.
echo ========================================
echo  Astro Data Visualization Setup
echo ========================================
echo.

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Instale Python 3.7+ primeiro.
    pause
    exit /b 1
)

echo [OK] Python detectado

REM Menu
echo.
echo Opcoes:
echo 1 - Instalacao completa
echo 2 - Apenas instalar dependencias
echo 3 - Apenas criar diretorios
echo 0 - Sair
echo.

set /p choice="Escolha uma opcao: "

if "%choice%"=="1" (
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt
    
    echo.
    echo Criando diretorios...
    if not exist data\raw mkdir data\raw
    if not exist data\processed mkdir data\processed
    if not exist notebooks mkdir notebooks
    
    echo.
    echo Executando exemplo...
    python examples\example1_basic.py
    
) else if "%choice%"=="2" (
    echo.
    pip install -r requirements.txt
    
) else if "%choice%"=="3" (
    echo.
    if not exist data\raw mkdir data\raw
    if not exist data\processed mkdir data\processed
    if not exist notebooks mkdir notebooks
    echo Diretorios criados!
    
) else if "%choice%"=="0" (
    echo Saindo...
) else (
    echo Opcao invalida!
)

pause
