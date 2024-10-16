from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import QPoint, QPropertyAnimation, QSequentialAnimationGroup, QSize, Qt
from PySide6.QtSvg import QSvgRenderer
import os

w = 70*3
h = 70
iconsize = 55
class UserTools(QWidget):
    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        #Main Layout
        self.main_layout = QHBoxLayout(self)

        #User Info
        self.setFixedSize(w, h)
        self.setStyleSheet("""
                           *{
                               background-color:none;
                               border-style:none;
                           }
                           QToolButton{
                               border-radius:20px;
                           }
                           """)
        #icons folder path
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')

        #Contact, Help, Setting,  button
        self.contact = QPushButton(self)
        self.help = QPushButton(self)
        self.setting = QPushButton(self)

        # Buttons names
        buttons = {self.contact:"contact", self.help:"help", self.setting:"setting"}

        # Set buttons
        for button, name in buttons.items():
            button.setObjectName(name)
            button.setFixedSize(iconsize, iconsize)
            button.setIconSize(QSize(iconsize, iconsize))
            button.setIcon(QIcon(f"{icons_dir}/{name}"))
            button.clicked.connect(self.toggleAnimation)
            self.main_layout.addWidget(button)

        self.setLayout(self.main_layout)

    def toggleAnimation(self):
        self.init_pos= self.sender().pos()
        x,y = self.init_pos.toTuple()
        self.final_pos = QPoint(x+2, y+2)

        self.ani = QPropertyAnimation(self.sender(), b"pos")
        self.ani.setEndValue(self.final_pos)
        self.ani.setDuration(50)

        self.ani2 = QPropertyAnimation(self.sender(), b"pos")
        self.ani2.setEndValue(self.init_pos)
        self.ani2.setDuration(50)

        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.ani)
        self.anim_group.addAnimation(self.ani2)
        self.anim_group.start()
