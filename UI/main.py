from PySide6.QtWidgets import QWidget, QApplication, QFrame
from PySide6.QtCore import Qt
from esr import ESR
from user import UserInfo
from profile import Profile
from background import Background

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        background = Background(self)
        background.move(0,0)
        esr = ESR(self)
        esr.move(550, 18)
        user_info = UserInfo(self, background, esr)
        user_info.move(25, 40)
        pro = Profile(self, user_info)
        pro.move(5, 18)


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
