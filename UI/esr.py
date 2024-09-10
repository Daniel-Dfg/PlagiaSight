from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QWidget, QFrame, QPushButton, QGraphicsDropShadowEffect, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import QSize, Qt
#from PySide6.QtSvg import QtSvgWidget


width = 130
height = 30
iconsize = 30
class ESR(QPushButton):
    def __init__(self, parent:QWidget=None) -> None:
        super().__init__(parent)
        #Parent QWidget
        self.parent = parent
        # Frame
        self.setObjectName("esr")
        self.resize(width, height)
        self.setStyleSheet("""
                           *{
                                background-color: none;
                                border-style: none; 
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
        exit.pressed.connect(self.parent.close)
        
        #Resize button
        resize = QPushButton(self)
        resize.setObjectName("resize")
        resize.setFixedSize(iconsize, iconsize)
        resize.setIcon(QIcon("./icons/resize.svg"))
        resize.setIconSize(QSize(iconsize, iconsize))
        resize.move(50, 2)
        #resize.pressed.connect(self.parent.showMaximized)
        
        #Reduce button
        reduce = QPushButton(self)
        reduce.setObjectName("reduce")
        reduce.setFixedSize(iconsize, iconsize)
        reduce.setIconSize(QSize(iconsize, iconsize))
        reduce.setIcon(QIcon("./icons/reduce.svg"))
        reduce.move(5, 0)
        reduce.pressed.connect(self.parent.showMinimized)
        
        
        
                