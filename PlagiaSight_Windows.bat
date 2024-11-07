@echo off

set SCRIPT_DIR=%~dp0

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install it before running Plagiasight via https://www.python.org/downloads/windows/
    exit /b
)

echo Activating virtual environment...
python -m venv "%SCRIPT_DIR%env"
call "%SCRIPT_DIR%env\Scripts\activate"
echo Virtual environment activated.

echo Installing dependencies (necessary for Plagiasight to run)...
pip install -r "%SCRIPT_DIR%requirements.txt"
echo Dependencies installed. Enjoy PlagiaSight !

python "%SCRIPT_DIR%src\main.py"

call "%SCRIPT_DIR%env\Scripts\deactivate"
