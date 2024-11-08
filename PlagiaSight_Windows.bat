@echo off

setlocal
set "SCRIPT_DIR=%~dp0"

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install it before running Plagiasight via https://www.python.org/downloads/windows/
    exit /b
)

if not exist "%SCRIPT_DIR%env\" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%env"
    echo Virtual environment created.
)

echo Activating virtual environment...
call "%SCRIPT_DIR%env\Scripts\activate"

pip freeze > "%SCRIPT_DIR%current_requirements.txt"
fc /B "%SCRIPT_DIR%current_requirements.txt" "%SCRIPT_DIR%requirements.txt" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies (necessary for Plagiasight to run)...
    pip install -r "%SCRIPT_DIR%requirements.txt"
    echo Dependencies installed.
) else (
    echo Dependencies are already up to date.
)

echo Launching PlagiaSight...
python "%SCRIPT_DIR%src\main.py"

call "%SCRIPT_DIR%env\Scripts\deactivate"

del "%SCRIPT_DIR%current_requirements.txt"

endlocal
