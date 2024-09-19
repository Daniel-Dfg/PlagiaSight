from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton, QFrame
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer

w = 722
h = 53
iconsize = 55
class UserTools(QFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        #UserInfo
        self.resize(w, h)
        self.setStyleSheet("""
                           *{
                               background-color:none;
                               border-style:none;
                           }
                           QToolButton{
                               border-radius:20px;
                           }

                           QToolButton#setting:hover{
                            }
                           QToolButton#help:hover{
                            }
                            QToolButton#contact:hover{

                            }
                            QToolButton#dark_mode:hover{
                            }
                           """)

        #Contact button
        contact = QToolButton(self)
        contact.setObjectName("contact")
        contact.setFixedSize(iconsize, iconsize)
        contact.setIconSize(QSize(iconsize, iconsize))
        contact.setIcon(QIcon("./icons/contact.svg"))
        contact.move(0,0)

        #Help button
        help = QToolButton(self)
        help.setObjectName("help")
        help.setFixedSize(iconsize, iconsize)
        help.setIcon(QIcon("./icons/help.svg"))
        help.setIconSize(QSize(iconsize, iconsize))
        help.move(80, 0)

        #Setting
        setting = QToolButton(self)
        setting.setObjectName("setting")
        setting.setFixedSize(iconsize+10, iconsize+10)
        setting.setIcon(QIcon("./icons/setting.svg"))
        setting.setIconSize(QSize(iconsize+10, iconsize+10))
        setting.move(150, 0)


        #Wifi
        wifi = QToolButton(self)
        wifi.setObjectName("wifi")
        wifi.setFixedSize(iconsize, iconsize)
        wifi.setIcon(QIcon("./icons/wifi.svg"))
        wifi.setIconSize(QSize(iconsize, iconsize))
        wifi.move(670, 0)
