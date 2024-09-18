from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QToolButton
from PySide6.QtCore import QSize, Qt
from PySide6.QtSvg import QSvgRenderer


width = 135
height = 35
iconsize = 35
class ESR(QToolButton):
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
                           QToolButton#exit:hover{
                            }
                            QToolButton#wresize:hover{
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
        self.wresize = QToolButton(self)
        self.wresize.setObjectName("resize")
        self.wresize.setFixedSize(iconsize, iconsize)
        self.wresize.setIcon(QIcon("./icons/resize.svg"))
        self.wresize.setIconSize(QSize(iconsize, iconsize))
        self.wresize.move(50, 0)
        self.wresize.pressed.connect(parent.showMaximized)
        
        #Reduce button
        reduce = QToolButton(self)
        reduce.setObjectName("reduce")
        reduce.setFixedSize(iconsize, iconsize)
        reduce.setIconSize(QSize(iconsize, iconsize))
        reduce.setIcon(QIcon("./icons/reduce.svg"))
        reduce.move(0, 0)
        reduce.pressed.connect(parent.showMinimized)
        
    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.wresize.pressed.connect(self.parent.showNormal)
        else: 
            self.wresize.pressed.connect(self.parent.showMaximized)    