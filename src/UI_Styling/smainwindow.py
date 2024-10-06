from PySide6.QtWidgets import QMainWindow, QWidget, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent


w = 790
h = 560
class SMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(w, h)
        self.background = QWidget()
        self.background.setObjectName("background")
        self.background.setStyleSheet("""
                           QWidget#background{
                                background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1,stop: 0 #100B2B,stop: 1 #473242);
                                border-radius:10px;
                                }""")
        self.setCentralWidget(self.background)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and not self.window().isMaximized():
            self.dragging = True
            self.offset = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        try:
            if self.dragging:
                new_pos = event.globalPosition().toPoint() - self.offset
                screen_geometry = QApplication.primaryScreen().geometry()
                window_geometry = self.geometry()
                if new_pos.x() < 0:
                    new_pos.setX(0)
                elif new_pos.x() + window_geometry.width() > screen_geometry.width():
                    new_pos.setX(screen_geometry.width() - window_geometry.width())

                if new_pos.y() < 0:
                    new_pos.setY(0)
                elif new_pos.y() + window_geometry.height() > screen_geometry.height():
                    new_pos.setY(screen_geometry.height() - window_geometry.height())

                # Move the window to the new position
                self.move(new_pos)
        except AttributeError:
            print("window drag could not started")

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
