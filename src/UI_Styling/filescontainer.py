from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from UI_Styling.slistwidget import SListWidget
w = 500
h = 340

class FilesContainer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(w, h)
        #Layout
        self.main_layout = QVBoxLayout(self)
        #Containers
        self.validContainer = SListWidget()
        self.invalidContainer = SListWidget()
        self.invalidContainer.label.setText("InValid Files:")
        self.main_layout.addWidget(self.validContainer, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.invalidContainer, alignment=Qt.AlignmentFlag.AlignBottom)
