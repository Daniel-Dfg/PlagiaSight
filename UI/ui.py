from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from esr import ESR
from user import UserInfo
from pro import Pro

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        background = QWidget(self)
        background.setStyleSheet("""
                                 background-color:#EEEEEE;
                                 border-radius:15px;
                                 """)
        background.setGeometry(0,0, 700, 550)
        esr = ESR(self)
        esr.setGeometry(550, 18, 0, 0)
        user_info = UserInfo(self)
        user_info.setGeometry(25, 40, 0, 0)
        pro = Pro(self)
        pro.setGeometry(5, 18, 0, 0)
        
        
    # Drag window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_start_pos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_start_pos)
            self.drag_start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_start_pos = None
        
if __name__== "__main__":
    app = QApplication()
    window = Window()
    window.show()
    app.exec()