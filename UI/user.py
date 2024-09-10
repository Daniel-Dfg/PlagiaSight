from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QFrame, QPushButton, QGraphicsDropShadowEffect, QWidget
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer

w = 722
h = 53
iconsize = 55
class UserInfo(QPushButton):
    def __init__(self, parent:QWidget) -> None:
        super().__init__(parent)
        #UserInfo
        self.resize(w, h)
        self.setStyleSheet("""
                           *{
                               background-color:none;
                               border-style:none;
                           }
                           QPushButton{
                               border-radius:20px;
                           }

                           QPushButton#setting:hover{
                            }
                           QPushButton#help:hover{
                            }
                            QPushButton#contact:hover{

                            }
                            QPushButton#dark_mode:hover{
                            }
                           """)
        
        #Contact button
        contact = QPushButton(self)
        contact.setObjectName("contact")
        contact.setFixedSize(iconsize, iconsize)
        contact.setIconSize(QSize(iconsize, iconsize))
        contact.setIcon(QIcon("./icons/contact.svg"))
        contact.move(0,0)
        
        #Help button
        help = QPushButton(self)
        help.setObjectName("help")
        help.setFixedSize(iconsize, iconsize)
        help.setIcon(QIcon("./icons/help.svg"))
        help.setIconSize(QSize(iconsize, iconsize))
        help.move(80, 0)

        #Setting
        setting = QPushButton(self)
        setting.setObjectName("setting")
        setting.setFixedSize(iconsize+10, iconsize+10)
        setting.setIcon(QIcon("./icons/setting.svg"))
        setting.setIconSize(QSize(iconsize+10, iconsize+10))
        setting.move(150, 0)
        
        
        #Wifi
        wifi = QPushButton(self)
        wifi.setObjectName("wifi")
        wifi.setFixedSize(iconsize, iconsize)
        wifi.setIcon(QIcon("./icons/wifi.svg"))
        wifi.setIconSize(QSize(iconsize, iconsize))
        wifi.move(670, 0)
        