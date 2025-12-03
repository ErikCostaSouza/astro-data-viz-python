@echo off
REM ============================================
REM MAST Data Downloader - Windows Helper
REM ============================================

setlocal enabledelayedexpansion

:menu
cls
echo.
echo ============================================
echo  ^^!MAST DATA DOWNLOADER - Menu Principal^^!
echo ============================================
echo.
echo 1. Listar arquivos FITS disponiveis
echo 2. Baixar dados de Hubble (M51)
echo 3. Baixar dados de Hubble (NGC 6543)
echo 4. Baixar dados de JWST (CEERS)
echo 5. Baixar + Processar com Pipeline
echo 6. Inspecionar metadados de arquivo FITS
echo 7. Executar exemplo completo
echo 8. Sair
echo.
set /p choice="Escolha uma opcao (1-8): "

if "%choice%"=="1" goto list_fits
if "%choice%"=="2" goto hubble_m51
if "%choice%"=="3" goto hubble_ngc
if "%choice%"=="4" goto jwst
if "%choice%"=="5" goto process
if "%choice%"=="6" goto inspect
if "%choice%"=="7" goto example
if "%choice%"=="8" goto exit
goto menu

:list_fits
cls
echo.
echo ============================================
echo  Lista de Arquivos FITS Disponiveis
echo ============================================
echo.
.\.venv\Scripts\python inspect_fits_metadata.py
pause
goto menu

:hubble_m51
cls
echo.
echo ============================================
echo  Baixando dados de M51 (Hubble)
echo ============================================
echo.
set /p limit="Quantos arquivos? (default 1): "
if "%limit%"=="" set limit=1
.\.venv\Scripts\python download_mast_data.py --target "M51" --limit %limit%
pause
goto menu

:hubble_ngc
cls
echo.
echo ============================================
echo  Baixando dados de NGC 6543 (Hubble)
echo ============================================
echo.
set /p limit="Quantos arquivos? (default 2): "
if "%limit%"=="" set limit=2
.\.venv\Scripts\python download_mast_data.py --target "NGC 6543" --limit %limit%
pause
goto menu

:jwst
cls
echo.
echo ============================================
echo  Baixando dados de JWST (CEERS)
echo ============================================
echo.
set /p limit="Quantos arquivos? (default 1): "
if "%limit%"=="" set limit=1
.\.venv\Scripts\python download_mast_data.py --source jwst --target "CEERS" --limit %limit%
pause
goto menu

:process
cls
echo.
echo ============================================
echo  Download + Processamento com Pipeline
echo ============================================
echo.
echo Opcoes:
echo 1. M51
echo 2. NGC 6543
echo 3. CEERS (JWST)
echo.
set /p target="Escolha alvo (1-3): "

if "%target%"=="1" (
    set "alvo=M51"
    set "source=hubble"
) else if "%target%"=="2" (
    set "alvo=NGC 6543"
    set "source=hubble"
) else if "%target%"=="3" (
    set "alvo=CEERS"
    set "source=jwst"
) else (
    echo Opcao invalida
    pause
    goto menu
)

set /p limit="Quantos arquivos? (default 1): "
if "%limit%"=="" set limit=1

echo Iniciando download e processamento de !alvo!...
.\.venv\Scripts\python download_mast_data.py --source %source% --target "!alvo!" --limit %limit% --process

pause
goto menu

:inspect
cls
echo.
echo ============================================
echo  Inspecionar Arquivo FITS
echo ============================================
echo.
set /p filepath="Caminho do arquivo FITS: "
.\.venv\Scripts\python inspect_fits_metadata.py "%filepath%" --verbose
pause
goto menu

:example
cls
echo.
echo ============================================
echo  Executar Exemplo Completo (4)
echo ============================================
echo.
echo Processando dados reais com multiplas
echo configuracoes...
echo.
.\.venv\Scripts\python examples\example4_real_data.py
pause
goto menu

:exit
echo.
echo Ate logo! Explore mais dados em https://archive.stsci.edu/
echo.
exit /b 0
