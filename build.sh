#!/bin/bash

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

pip install pyinstaller

pyinstaller --onefile \
            --name PlagiaSight \
            --add-data "src/UI_Styling:UI_Styling" \
            --add-data "src/UI_Functional:UI_Functional" \
            --add-data "src/temp:temp" \
            --collect-submodules nltk \
            --collect-submodules PySide6 \
            --collect-submodules googlesearch \
            --add-data "src/__init__.py:." \
            --add-data "src/text_analysis.py:." \
            --add-data "src/web_scraper.py:." \
            --paths src \
            --windowed \
            src/main.py

mkdir -p dist/temp
cp src/temp/README.md dist/temp/

deactivate
