@echo off

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install it before running Plagiasight via https://www.python.org/downloads/windows/
    exit /b
)

echo Activating virtual environment...
python -m venv env
call env\Scripts\activate
echo Virtual environment activated.
echo Installing dependencies (necessary for Plagiasight to run)...
pip install -r requirements.txt
echo Dependencies installed. Enjoy PlagiaSight !

python src\main.py

call env\Scripts\deactivate
