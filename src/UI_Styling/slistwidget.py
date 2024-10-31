from PySide6.QtWidgets import QListWidget

w = 440
h = 130
class SListWidget(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(w, h)
        self.setStyleSheet("""
            *{
            border-radius:10px;
            background-color: rgba(255, 255, 255, 25);
            }
            """)
