from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from esr import ESR
from user import UserInfo
from profile import Profile

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        background = QWidget(self)
        background.setStyleSheet("""
                                 background-color:#DDDDDD;
                                 border-radius:15px;
                                 """)
        background.setGeometry(0,0, 700, 550)
        esr = ESR(self)
        esr.setGeometry(550, 18, 0, 0)
        user_info = UserInfo(self)
        user_info.move(25, 40)
        pro = Profile(self, user_info)
        pro.setGeometry(5, 18, 0, 0)


    # Drag window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        try:
            if self.drag_start_pos:
                self.move(self.pos() + event.globalPosition().toPoint() - self.drag_start_pos)
                self.drag_start_pos = event.globalPosition().toPoint()
        except AttributeError:
            print("drag_start_pos couldn't start")

    def mouseReleaseEvent(self, event):
        self.drag_start_pos = None

if __name__== "__main__":
    app = QApplication()
    window = Window()
    window.show()
    app.exec()
