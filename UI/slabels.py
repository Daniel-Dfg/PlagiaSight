import os
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QLabel, QWidget


class SLabels(QLabel):
    """
    - Special label
    """
    def __init__(self, text:str, parent:QWidget= None) -> None:
        super().__init__(text,parent)
        self.setStyleSheet("""
                           *{
                               background-color:none;
                               border-style:none;
                               color:#BBF1F5;
                               font-size: none;
                           }
                           """)
        # Set the font path on the OS
        font_dir = 'fonts'
        font_path = os.path.join(font_dir, 'AllertaStencil-Regular.ttf')

        if not os.path.exists(font_path):
            print(f"Error: Font file not found at {font_path}")
            return
        
        # Set the font
        font = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font)[-1]
        self.setFont(QFont(font_family))
