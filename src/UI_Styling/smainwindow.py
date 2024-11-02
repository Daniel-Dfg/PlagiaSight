from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent

from UI_Styling.stitlebar import STitleBar


w = 790
h = 560
class SMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.get_in_touch_window = None
        self.help_window = None
        #Window can't be resized more then that
        self.setMinimumSize(w, h)

        # Set Window to the center
        screen = self.screen().size()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,(screen.height() - size.height())//2)

        # Window Flages
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the central background
        self.background = QWidget()
        self.background.setObjectName("background")
        self.background.setStyleSheet("""
                           QWidget#background{
                                background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1,stop: 0 #100B2B,stop: 1 #473242);
                                border-radius:10px;
                                }""")

        self.main_layout = QVBoxLayout(self.background)
        self.titleBar = STitleBar(self)
        self.titleBar.exit.clicked.connect(self.closeAll)
        self.main_layout.addWidget(self.titleBar, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.setCentralWidget(self.background)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and not self.window().isMaximized():
            self.dragging = True
            self.offset = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        try:
            if self.dragging:
                new_pos = event.globalPosition().toPoint() - self.offset
                # Move the window to the new position
                self.move(new_pos)

        except AttributeError:
            print("window drag could not started")

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def closeAll(self):
        self.close()
        if (self.get_in_touch_window):
            self.get_in_touch_window.close()
        if (self.help_window):
            self.help_window.close()
