import sys
from PySide6.QtWidgets import QApplication, QLabel, QGraphicsBlurEffect, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from BlurWindow.blurWindow import blur

class GlassBlurWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
                           QWidget{
                               background-color:rgba(0, 0, 0, 100);
                           }
                           """)
        blur(self.winId())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlassBlurWindow()
    window.show()
    sys.exit(app.exec())
