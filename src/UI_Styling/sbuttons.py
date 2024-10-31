from PySide6.QtGui import QColor, QRgba64
from PySide6.QtWidgets import QPushButton, QWidget, QGraphicsDropShadowEffect

w = 130
h = 50
class SButtons(QPushButton):
    """
    - Special button
    """
    def __init__(self, text:str= None, parent:QWidget= None) -> None:
        super().__init__(text, parent)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(4.0)
        shadow.setYOffset(4.0)
        shadow.setXOffset(0)
        shadow.setColor(QColor(0, 0, 0, 64))
        self.setGraphicsEffect(shadow)
        self.setFixedSize(w, h)
        self.setStyleSheet("""
                           QPushButton{
                               background-color:#3E3182;
                               border-radius:4;
                               color: white;
                               font-size: 18px;
                           }
                           QPushButton::hover{
                               background-color:#382F9C;
                           }
                           """)
