from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath
from PySide6.QtCore import QRect, Qt
from nltk.metrics.aline import align
from UI_Styling.sbuttons import SButtons

w =300
h = 330
class SDropArea(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(w, h)
        self.setText(f"Drag and Drop\n To\n Upload{'\n'*5}")
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            *{
                color: rgba(255, 255, 255, 100);
                background-color: rgba(255, 255, 255, 25);
                border-radius: 14px;
                font-size: 24px;
            }
            """)
        self.vbox = QVBoxLayout(self)

        #BrowseFiles
        self.browseFiles = SButtons("Browse Files", self)
        self.vbox.addStretch()
        self.vbox.addWidget(self.browseFiles, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

        #BrowseFolders
        self.browseFolders= SButtons("Browse Folders", self)
        self.browseFolders.setDisabled(True)
        self.browseFolders.setHidden(True)
        self.vbox.addWidget(self.browseFolders, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        self.vbox.addSpacing(20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(QRect(2, 2, 295,325), 10, 10)  # Adjust radius as needed

        # Set pen for dashed border with custom dash pattern
        pen = QPen(QColor(255, 255, 255, 128), 3)
        pen.setDashPattern([2, 2])  # Adjust dash length and spacing as needed
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)
        painter.strokePath(path, pen)

        # Paint the label's text
        super().paintEvent(event)
