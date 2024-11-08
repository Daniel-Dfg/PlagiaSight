from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent

from UI_Styling.stitlebar import STitleBar


class SMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        w = self.screen().size().width()
        h = self.screen().size().height()

        #Window can't be resized more then that
        self.setMinimumSize(int(w/1.5), int(h/1.1))
        self.get_in_touch_window = None
        self.help_window = None
        self.graph_window = None
        self.results_window = None
        self.setStyleSheet("""
                            *{
                            background-color: rgba(0,0, 0, 0);
                            border:none;
                            font-size:15px;
                            }
                            QComboBox {
                                font-size:18px;
                                height: 30px;
                                background-color:#3E3182;
                                border-radius:3px;

                            }
                            QComboBox:hover{
                                height: 30px;
                                background-color:#3E3182;
                                border-radius:3px;

                            }
                            QComboBox::drop-down{
                                width:0px;
                                background-color:rgba(0, 0, 0, 0);
                            }

                            QComboBox QAbstractItemView {
                                background-color: #5D5A85;
                                color: black;
                            }

                           QWidget#background{
                                background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1,stop: 0 #100B2B,stop: 1 #473242);
                                border-radius:10px;
                                }""")

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
        if (self.graph_window):
            self.graph_window.close()
        if (self.results_window):
            self.results_window.close()
