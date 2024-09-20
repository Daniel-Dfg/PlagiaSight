from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
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
        self.container = QWidget(self)
        self.container.setGeometry(20, 20, 800, 600)

        layout = QVBoxLayout(self.container)
        
        # background
        background = Background()
        self.setCentralWidget(background)

        #Exit reSize Reduce
        self.esr = ESR(self)
        self.esr.move(630, 15)


        # User Tools
        user_info = UserTools(self)
        user_info.move(20, 490)

        # Special buttons
        self.sb1 = SButtons("One file with related online data",self)
        self.sb1.move(180, 300)
        self.sb2 = SButtons("A set of files between each other",self)
        self.sb2.move(180, 380)

        #Special Labels
        self.sl1 = SLabels("PlagiaEye", self)

        self.sl1.setStyleSheet(self.sl1.styleSheet().replace("font-size: none;", "font-size: 64px;"))
        self.sl1.move(230, 50)
        self.sl1.setFixedSize(350, 100)
        self.sl2 = SLabels("A transparent plagiarism detection tool.", self)
        self.sl2.setStyleSheet(self.sl2.styleSheet().replace("font-size: none;", "font-size: 24px;"))
        self.sl2.move(150, 150)
        self.sl2.setFixedSize(500, 100)
        self.sl3 = SLabels("Compare...", self)
        self.sl3.setStyleSheet(self.sl3.styleSheet().replace("font-size: none;", "font-size: 36px;"))
        self.sl3.move(290, 230)
        self.sl3.setFixedSize(500, 50)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.AdjustUIWhenMaximized)
        self.timer.start(100)

        
    def AdjustUIWhenMaximized(self):
            if self.esr.switch:
                self.esr.move(1000, 248)
                self.sb1.move(580, 700)
                self.sb2.move(580, 780)
                print("im here")
                
        

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
