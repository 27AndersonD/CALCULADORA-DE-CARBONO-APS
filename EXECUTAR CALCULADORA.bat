@echo off
echo ============================================
echo  Calculadora de Carbono Avançada - UNIP
echo ============================================
echo.
echo Verificando dependências...
pip install -r requirements.txt
echo.
echo Iniciando a aplicação no navegador...
streamlit run app/main.py
pause