from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QWidget
class Background(QFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.resize(700, 550)
        self.setStyleSheet("""         
                        background-color:#DDDDDD;
                        border-radius:15px;
                                 """)