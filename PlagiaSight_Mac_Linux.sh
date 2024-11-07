#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it via https://www.python.org/downloads/"
    exit
fi

echo "Activating virtual environment..."
python3 -m venv "$SCRIPT_DIR/venv"
source "$SCRIPT_DIR/venv/bin/activate"
echo "Virtual environment activated."

echo "Installing dependencies (necessary for Plagiasight to run)..."
pip install -r "$SCRIPT_DIR/requirements.txt"
echo "\n\nDependencies installed. Enjoy PlagiaSight !"

python3 "$SCRIPT_DIR/src/main.py"

deactivate
