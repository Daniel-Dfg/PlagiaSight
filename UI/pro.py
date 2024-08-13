from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer

class Pro(QPushButton):
    def __init__(self, parent: QWidget= None) -> None:
        super().__init__(parent)
        size = 75
        self.setStyleSheet("""
                           *{
                               background-color:rgba(0, 0, 0, 0);
                               border-style:none;
                           }
                           QPushButton#profile:hover{
                               icon:url(./icons/profileGlow.svg);
                           }
                           """)
        self.setFixedSize(size+10, size+10)
        self.setIcon(QIcon("./icons/profile.svg"))
        self.setIconSize(QSize(size, size))
        self.setObjectName("profile")