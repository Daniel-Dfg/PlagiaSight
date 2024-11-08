#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it via https://www.python.org/downloads/"
    exit 1
fi

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "Virtual environment created."
fi

echo "Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

if ! pip freeze | grep -qF "$(cat "$SCRIPT_DIR/requirements.txt")"; then
    echo "Installing dependencies (necessary for Plagiasight to run)..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
    echo "Dependencies installed."
else
    echo "Dependencies already installed."
fi

echo -e "\nLaunching PlagiaSight..."
python3 "$SCRIPT_DIR/src/main.py"

deactivate
