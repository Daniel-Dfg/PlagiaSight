from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QToolButton, QHBoxLayout
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer
from os import path


width = 200
height = 40
iconsize = 35
class STitleBar(QWidget):
    def __init__(self, parent:QWidget= None) -> None:
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)

        # Frame
        self.setObjectName("titlBar")

        self.setStyleSheet("""
                           *{
                                background-color: none;
                                border-style:none;
                           }
                           """)
        icons_dir = path.join(path.dirname(__file__), 'icons')

        #Exit, max, min button
        self.exit = QToolButton()
        self.maxi = QToolButton()
        self.mini = QToolButton()

        #List buttons functionalities
        buttons = {self.mini:(self.window().showMinimized, "mini"),
            self.maxi:(self.switchSize,"maxi"),
            self.exit:(None,"exit" )}

        for button, func in buttons.items():
            if (button != self.exit):
                button.pressed.connect(func[0])
            button.setObjectName(func[1])
            self.main_layout.addSpacing(15)
            button.setFixedSize(iconsize, iconsize)
            button.setIcon(QIcon(f"{icons_dir}/{func[1]}.svg"))
            button.setIconSize(QSize(iconsize, iconsize))
            self.main_layout.addWidget(button)


        self.setLayout(self.main_layout)


    def switchSize(self):
        if not self.window().isMaximized():
            self.window().showMaximized()
            self.switch = True
        else:
            self.window().showNormal()
            self.switch = False
