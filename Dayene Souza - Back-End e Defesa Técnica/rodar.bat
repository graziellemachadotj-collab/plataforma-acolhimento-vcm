@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  Plataforma de Acolhimento - API
echo  ================================
where python >nul 2>nul || (echo  Instale o Python 3.10+ em https://www.python.org/downloads/ marcando "Add python.exe to PATH". & pause & exit /b 1)
if not exist ".venv\Scripts\python.exe" (
  echo  Preparando o ambiente pela primeira vez...
  python -m venv .venv || (pause & exit /b 1)
  ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
  ".venv\Scripts\python.exe" -m pip install --progress-bar on -r requirements.txt || (pause & exit /b 1)
)
".venv\Scripts\python.exe" rodar.py %*
pause
