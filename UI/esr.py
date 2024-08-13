from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QWidget, QFrame, QPushButton, QGraphicsDropShadowEffect, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import QSize, Qt
from PySide6.QtSvg import  QtSvg


width = 125
height = 25

class ESR(QFrame):
    def __init__(self, parent:QWidget=None) -> None:
        super().__init__(parent)
        #Parent QWidget
        self.parent = parent
        # Frame
        self.setFixedSize(width, height)
        self.setStyleSheet("""
                           *{
                                background-color: #2E5C6F;
                                border-radius: 8px;
                                border-style: none;
                           }
                           QPushButton{
                               background-color:#2E5C6F;
                           }
                           QPushButton#exit:hover{

                                background-image:url(./icons/closeGlow.svg)
                            }
                            QPushButton#resize:hover{
                                background-image:url(./icons/resizeGlow.svg);
                            }
                            QPushButton#reduce:hover{
                                background-image:url(./icons/reduceGlow.svg)
                            }
                           """)
        
        #Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor("black"))
        self.setGraphicsEffect(shadow)
        
        #Exit button
        exit = QPushButton()
        exit.setObjectName("exit")
        exit.setFixedSize(25, 25)
        exit.setIcon(QIcon("./icons/close.svg"))
        exit.setIconSize(QSize(25, 25))
        exit.pressed.connect(self.parent.close)
        
        #Resize button
        resize = QPushButton()
        resize.setObjectName("resize")
        resize.setFixedSize(20, 20)
        resize.setIcon(QIcon("./icons/resize.svg"))
        resize.setIconSize(QSize(20, 20))
        resize.pressed.connect(self.parent.showMaximized)
        
        #Reduce button
        reduce = QPushButton()
        reduce.setObjectName("reduce")
        reduce.setFixedSize(20, 20)
        reduce.setIconSize(QSize(20, 20))
        reduce.setIcon(QIcon("./icons/reduce.svg"))
        reduce.pressed.connect(self.parent.showMinimized)
        
        #HBOX
        hbox = QHBoxLayout(self)
        hbox.addWidget(reduce)
        hbox.addWidget(resize)
        hbox.addWidget(exit)
        hbox.setContentsMargins(0, 0, 0 ,0)
        
                