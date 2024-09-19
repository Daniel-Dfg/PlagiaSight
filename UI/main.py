from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from esr import ESR
from userTools import UserTools
from sbuttons import SButtons
from slabels import SLabels
from background import Background

w = 790
h = 560
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(w, h)
        
        # background
        background = Background()
        self.setCentralWidget(background)

        #Exit reSize Reduce
        esr = ESR(self)
        esr.move(630, 15)

        # User Tools
        user_info = UserTools(self)
        user_info.move(20, 490)

        # Special buttons
        sb1 = SButtons("One file with related online data",self)
        sb1.move(180, 300)
        sb2 = SButtons("A set of files between each other",self)
        sb2.move(180, 380)

        #Special Labels
        sl1 = SLabels("PlagiaEye", self)

        sl1.setStyleSheet(sl1.styleSheet().replace("font-size: none;", "font-size: 64px;"))
        sl1.move(230, 50)
        sl1.setFixedSize(350, 100)
        sl2 = SLabels("A transparent plagiarism detection tool.", self)
        sl2.setStyleSheet(sl2.styleSheet().replace("font-size: none;", "font-size: 24px;"))
        sl2.move(150, 150)
        sl2.setFixedSize(500, 100)
        sl3 = SLabels("Compare...", self)
        sl3.setStyleSheet(sl3.styleSheet().replace("font-size: none;", "font-size: 36px;"))
        sl3.move(290, 230)
        sl3.setFixedSize(500, 50)

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
