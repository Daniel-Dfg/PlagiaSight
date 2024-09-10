from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QLabel, QWidget


class SLabels(QLabel):
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
        font = QFontDatabase.addApplicationFont("./font/AllertaStencil-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font)[0]
        self.setFont(QFont(font_family))
        