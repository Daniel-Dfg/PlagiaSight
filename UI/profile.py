from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QWidget, QPushButton
from PySide6.QtCore import QRect, QSize, QPropertyAnimation, QPoint, QRect
from PySide6.QtSvg import QSvgGenerator
size = 75
class Profile(QPushButton):
    def __init__(self, parent, child):
        super().__init__(parent, child)
        self.user = child
        self.uh = self.user.height()
        self.setStyleSheet("""
                           *{
                               background-color:rgba(0, 0, 0, 0);
                               border-style:none;
                           }
                           QPushButton#profile{
                               icon:url(./icons/profile.svg);
                           }
                           QPushButton#profile:hover{
                               icon:url(./icons/profileGlow.svg);
                           }
                           """)
        self.resize(size+10, size+10)
        self.setIconSize(QSize(size, size))
        self.setObjectName("profile")
        self.pressed.connect(self.up)

    def up(self):
        self.animation = QPropertyAnimation(self.user, b"size")
        if self.user.height() == self.uh:
            self.animation.setEndValue(QSize(self.user.width(), 50))
            self.animation.setDuration(200)
            self.animation.start()
        else:
            self.animation.setEndValue(QSize(self.user.width(), self.uh))
            self.animation.setDuration(200)
            self.animation.start()
