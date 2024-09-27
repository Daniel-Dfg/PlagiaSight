from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton, QWidget, QHBoxLayout
from PySide6.QtCore import QSize, Qt
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
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
        #Contact, Help, Setting,  button
        self.contact = QToolButton(self)
        self.help = QToolButton(self)
        self.setting = QToolButton(self)

        names = ["contact", "help", "setting"]
        buttons = [self.contact, self.help, self.setting]

        for i in range(3):
            buttons[i].setObjectName("setting")
            buttons[i].setFixedSize(iconsize, iconsize)
            buttons[i].setIconSize(QSize(iconsize, iconsize))
            buttons[i].setIcon(QIcon(f"{icons_dir}/{names[i]}"))
            self.main_layout.addWidget(buttons[i])

        self.setLayout(self.main_layout)
