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
        #icons folder path
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')

        #Contact, Help, Setting,  button
        self.contact = QToolButton(self)
        self.help = QToolButton(self)
        self.setting = QToolButton(self)

        # Buttons names
        buttons = {self.contact:"contact", self.help:"help", self.setting:"setting"}

        # Set buttons
        for button, name in buttons.items():
            button.setObjectName("setting")
            button.setFixedSize(iconsize, iconsize)
            button.setIconSize(QSize(iconsize, iconsize))
            button.setIcon(QIcon(f"{icons_dir}/{name}"))
            self.main_layout.addWidget(button)
        del buttons
        self.setLayout(self.main_layout)
