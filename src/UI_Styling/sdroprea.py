from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath
from PySide6.QtCore import Qt

class SDropArea(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 10);
                border-radius: 9px;
            }
            """)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 10, 10)  # Adjust radius as needed

        # Set pen for dashed border with custom dash pattern
        pen = QPen(QColor(255, 255, 255), 5)
        pen.setDashPattern([3, 3])  # Adjust dash length and spacing as needed
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)
        painter.strokePath(path, pen)

        # Paint the label's text
        super().paintEvent(event)
