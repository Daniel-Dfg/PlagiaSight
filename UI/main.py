from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import Qt
from stitlebar import STitleBar
from userTools import UserTools
from sbuttons import SButtons
from slabels import SLabels
from smainwindow import SMainWindow

w = 790
h = 560
class Window(SMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(w, h)
        
        
        # Layout
        vbox = QVBoxLayout()
        
        #Exit reSize Reduce
        esr = STitleBar(self)
        
        # User Tools
        user_info = UserTools(self)

        # Special buttons
        sb1 = SButtons("One file with related online data",self)
        sb2 = SButtons("A set of files between each other",self)

        #Special Labels
        sl1 = SLabels("PlagiaEye", self)

        sl1.setStyleSheet(sl1.styleSheet().replace("font-size: none;", "font-size: 64px;"))
        sl1.setFixedSize(350, 100)
        sl2 = SLabels("A transparent plagiarism detection tool.", self)
        sl2.setStyleSheet(sl2.styleSheet().replace("font-size: none;", "font-size: 24px;"))
        sl2.setFixedSize(500, 100)
        sl3 = SLabels("Compare...", self)
        sl3.setStyleSheet(sl3.styleSheet().replace("font-size: none;", "font-size: 36px;"))
        sl3.setFixedSize(500, 50)
        
        for i in [esr, user_info, sb1, sb2, sl1, sl2, sl3]:
            vbox.addWidget(i)
        self.centralWidget().setLayout(vbox)

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
