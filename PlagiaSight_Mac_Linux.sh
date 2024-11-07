#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it via https://www.python.org/downloads/"
    exit
fi

echo "Activating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Virtual environment activated."
echo "Installing dependencies (necessary for Plagiasight to run)..."
pip install -r requirements.txt
echo "Dependencies installed. Enjoy PlagiaSight !"

python3 src/main.py

deactivate

