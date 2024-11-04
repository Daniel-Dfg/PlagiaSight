from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout

class SListWidget(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("SListWidget")
        self.main_layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.container = QListWidget(self)
        self.main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop |Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.container)
        self.setStyleSheet("""
            *{
            border:none;
            background:none;
            border-radius: 10px;
            color: rgba(255, 255, 255, 100);
            font-size: 18px;
            }
            QLabel#SListWidget{
            background-color:rgba(255,255, 255, 25);
            }
            QListWidget{
            background-color:rgba(0, 0, 0, 0);
            }

            """)
