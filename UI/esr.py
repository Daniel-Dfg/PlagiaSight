from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QToolButton
from PySide6.QtCore import QSize, Qt
from PySide6.QtSvg import QSvgRenderer


width = 135
height = 35
iconsize = 35
class ESR(QToolButton):
    def __init__(self, parent:QWidget= None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.switch = False
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
                           QToolButton#exit:hover{
                            }
                            QToolButton#windowSize:hover{
                            }
                            QToolButton#reduce:hover{
                            }
                           """)
        
        #Exit button
        exit = QToolButton(self)
        exit.setObjectName("exit")
        exit.setFixedSize(iconsize,iconsize)
        exit.setIcon(QIcon("./icons/close.svg"))
        exit.setIconSize(QSize(iconsize, iconsize))
        exit.move(100, 0)
        exit.pressed.connect(parent.close)
        
        #Resize button
        self.windowSize = QToolButton(self)
        self.windowSize.setObjectName("resize")
        self.windowSize.setFixedSize(iconsize, iconsize)
        self.windowSize.setIcon(QIcon("./icons/resize.svg"))
        self.windowSize.setIconSize(QSize(iconsize, iconsize))
        self.windowSize.move(50, 0)
        self.windowSize.pressed.connect(self.switchSize)
        
        #Reduce button
        reduce = QToolButton(self)
        reduce.setObjectName("reduce")
        reduce.setFixedSize(iconsize, iconsize)
        reduce.setIconSize(QSize(iconsize, iconsize))
        reduce.setIcon(QIcon("./icons/reduce.svg"))
        reduce.move(0, 0)
        reduce.pressed.connect(parent.showMinimized)
        
    def switchSize(self):
        if not self.switch:
            self.parent.showMaximized()
            self.switch = True
        else: 
            self.parent.showNormal()
            self.switch = False