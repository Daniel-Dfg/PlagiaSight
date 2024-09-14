from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QWidget
from PySide6.QtGui import QLinearGradient
w = 790
h = 560
class Background(QFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.resize(w, h)
        self.setStyleSheet("""         
                        background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1,stop: 0 #2B2B2B,stop: 1 #413439);
                        border-radius:10px;
                                 """)