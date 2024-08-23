from PySide6.QtWidgets import QFrame, QPushButton, QWidget
from BlurWindow.blurWindow import GlobalBlur
from PySide6.QtGui import Qt
width = 760
height = 570
class Greetings(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
                           *{
                                color: rgb(255, 255, 255);
                                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:760, y2:570, stop:0 rgb(20, 20, 20), stop:1 rgb(50, 50, 50));
                                border-style: solid;
                                border-radius:21px;
                                }
                           """)
        self.setFixedSize(width, height)
        GlobalBlur(self.winId())