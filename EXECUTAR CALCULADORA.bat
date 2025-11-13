@echo off
echo ================================================
echo      Iniciando Calculadora de Carbono 🌿
echo ================================================

:: Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado! 
    echo Instale o Python antes de continuar.
    pause
    exit /b
)

:: Cria o ambiente virtual se nao existir
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: Ativa o ambiente virtual
call venv\Scripts\activate

:: Instala dependencias
echo Instalando dependencias...
pip install -r requirements.txt

:: Executa o programa
echo Iniciando o programa...
streamlit run app/main.py

pause