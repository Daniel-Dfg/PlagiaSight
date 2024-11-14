#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

SCRIPT_DIR=$(dirname "$(realpath "$0")")
# Ensure the script is run from the project root
cd "$SCRIPT_DIR"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it via https://www.python.org/downloads/"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "Virtual environment created."
fi

echo "Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies (necessary for PlagiaSight to run)..."
pip install -r "$SCRIPT_DIR/requirements.txt"
echo "Dependencies installed."

echo -e "\nLaunching PlagiaSight..."
python3 "$SCRIPT_DIR/src/main.py"

# Deactivate the virtual environment after the script completes
deactivate