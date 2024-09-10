from PySide6.QtWidgets import QWidget, QApplication, QFrame
from PySide6.QtCore import Qt
from esr import ESR
from user import UserInfo
from sbuttons import SButtons
from slabels import SLabels
from background import Background

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        background = Background(self)
        background.move(0,0)
        esr = ESR(self)
        esr.move(630, 15)
        user_info = UserInfo(self)
        user_info.move(20, 490)
        sb1 = SButtons("One file with related online data",self)
        sb1.move(180, 300)
        sb2 = SButtons("A set of files between each other",self)
        sb2.move(180, 380)
        sl1 = SLabels("PlagiaEye", self)
        sl1.setStyleSheet(sl1.styleSheet().replace("font-size: none;", "font-size: 64px;"))
        sl1.move(230, 50)
        sl2 = SLabels("A transparent plagiarism detection tool.", self)
        sl2.setStyleSheet(sl2.styleSheet().replace("font-size: none;", "font-size: 24px;"))
        sl2.move(150, 150)
        sl3 = SLabels("Compare...", self)
        sl3.setStyleSheet(sl3.styleSheet().replace("font-size: none;", "font-size: 36px;"))
        sl3.move(290, 230)
        
        
        


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
