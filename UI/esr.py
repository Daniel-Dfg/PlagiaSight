from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QFrame, QToolButton
from PySide6.QtCore import QSize, QPropertyAnimation, QRect
from PySide6.QtSvg import QSvgRenderer


width = 135
height = 35
iconsize = 35
class ESR(QPushButton):
    def __init__(self, parent:QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        # Frame
        self.setObjectName("esr")
        self.resize(width, height)
        self.setStyleSheet("""
                           *{
                                background-color: none;
                                border-style:none;
                                
                           }
                           QFrame#esr{
                           }
                           QPushButton#exit:hover{
                            }
                            QPushButton#resize:hover{
                            }
                            QPushButton#reduce:hover{
                            }
                           """)
        
        #Exit button
        exit = QPushButton(self)
        exit.setObjectName("exit")
        exit.setFixedSize(iconsize,iconsize)
        exit.setIcon(QIcon("./icons/close.svg"))
        exit.setIconSize(QSize(iconsize, iconsize))
        exit.move(100, 0)
        exit.pressed.connect(parent.close)
        
        #Resize button
        resize = QPushButton(self)
        resize.setObjectName("resize")
        resize.setFixedSize(iconsize, iconsize)
        resize.setIcon(QIcon("./icons/resize.svg"))
        resize.setIconSize(QSize(iconsize, iconsize))
        resize.move(50, 0)
        resize.pressed.connect(self.maxi)
        
        #Reduce button
        reduce = QPushButton(self)
        reduce.setObjectName("reduce")
        reduce.setFixedSize(iconsize, iconsize)
        reduce.setIconSize(QSize(iconsize, iconsize))
        reduce.setIcon(QIcon("./icons/reduce.svg"))
        reduce.move(0, 0)
        reduce.pressed.connect(parent.showMinimized)
        
    def maxi(self):
        pass
        
        
                