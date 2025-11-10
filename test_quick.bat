@echo off
REM Script de teste rápido para Windows
REM Testa o PathFinder A* sem necessitar Pygame

echo ======================================================================
echo TESTE RAPIDO - PATHFINDER A* (Windows)
echo ======================================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python de https://python.org
    echo Durante a instalacao, marque "Add Python to PATH"
    pause
    exit /b 1
)

echo Executando testes...
echo.

python test_quick.py

if errorlevel 1 (
    echo.
    echo ======================================================================
    echo ERRO: Alguns testes falharam!
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo SUCESSO: Todos os testes passaram!
    echo ======================================================================
)

echo.
echo Para testar com interface grafica (GUI):
echo   1. Crie ambiente virtual: python -m venv venv
echo   2. Ative: venv\Scripts\activate.bat
echo   3. Instale pygame: pip install pygame
echo   4. Execute: python main.py --example 1
echo.

pause
