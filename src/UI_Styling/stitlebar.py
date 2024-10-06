from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QToolButton, QHBoxLayout
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer
import os


width = 200
height = 40
iconsize = 35
class STitleBar(QWidget):
    def __init__(self, parent:QWidget= None) -> None:
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)

        # Frame
        self.setObjectName("titlBar")
        self.setFixedSize(width, height)
        self.setStyleSheet("""
                           *{
                                background-color: none;
                                border-style:none;
                           }
                           """)
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')

        #Exit, max, min button
        self.exit = QToolButton(self)
        self.maxi = QToolButton(self)
        self.mini = QToolButton(self)

        #List buttons functionalities
        buttons = {self.mini:(self.window().showMinimized, "mini"),
            self.maxi:(self.switchSize,"maxi"),
            self.exit:(self.window().close,"exit" )}

        for button, func in buttons.items():
            button.pressed.connect(func[0])
            button.setObjectName(func[1])
            button.setFixedSize(iconsize, iconsize)
            button.setIcon(QIcon(f"{icons_dir}/{func[1]}.svg"))
            button.setIconSize(QSize(iconsize, iconsize))
            self.main_layout.addWidget(button)
        del buttons
        self.setLayout(self.main_layout)


    def switchSize(self):
        if not self.window().isMaximized():
            self.window().showMaximized()
            self.switch = True
        else:
            self.window().showNormal()
            self.switch = False
