from PySide6.QtWidgets import QFrame
class Background(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setStyleSheet("""         
                        background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1,stop: 0 #2B2B2B,stop: 1 #413439);
                        border-radius:10px;
                                 """)