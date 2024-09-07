from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QFrame, QPushButton, QGraphicsDropShadowEffect, QWidget
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer

rec_size = (45, 480)
class UserInfo(QPushButton):
    def __init__(self, parent:QWidget, child1:QFrame, child2:QFrame) -> None:
        super().__init__(parent, child1, child2)
        #children
        self.child1 = child1 #background
        self.child2 = child2 #esr
        self.switch = True 
        #UserInfo
        self.resize(rec_size[0], rec_size[1])
        self.setStyleSheet("""
                           *{
                               background-color:#2E5C6F;
                               border-style:none;
                           }
                           QPushButton{
                               border-radius:20px;
                           }

                           QPushButton#setting:hover{
                                icon:url(./icons/settingGlow.svg);
                            }
                           QPushButton#help:hover{
                                icon:url(./icons/helpGlow.svg);
                            }
                            QPushButton#contact:hover{
                                icon:url(./icons/contactGlow.svg);
                            }
                            QPushButton#dark_mode:hover{
                                icon:url(./icons/darkmodeGlow.svg);
                            }
                           """)

        #Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor("black")
        self.setGraphicsEffect(shadow)

        #Up
        #Setting
        setting = QPushButton(self)
        setting_size= 30
        setting.setObjectName("setting")
        setting.setFixedSize(setting_size, setting_size)
        setting.setIcon(QIcon("./icons/setting.svg"))
        setting.setIconSize(QSize(setting_size, setting_size))
        setting.move(7, 60)

        #Wifi
        wifi = QPushButton(self)
        wifi_size= 30
        wifi.setObjectName("wifi")
        wifi.setFixedSize(wifi_size, wifi_size)
        wifi.setIcon(QIcon("./icons/wifi.svg"))
        wifi.setIconSize(QSize(wifi_size, wifi_size))
        wifi.move(8, 100)

        #Down
        #DarkMode
        dark_mode = QPushButton(self)
        dark_mode_size = 35
        dark_mode.setObjectName("dark_mode")
        dark_mode.setFixedSize(dark_mode_size, dark_mode_size)
        dark_mode.setIconSize(QSize(dark_mode_size, dark_mode_size))
        dark_mode.setIcon(QIcon("./icons/darkmode.svg"))
        dark_mode.move(4, 330)
        dark_mode.pressed.connect(self.dark)

        #Contact button
        contact = QPushButton(self)
        contact_size = 28
        contact.setObjectName("contact")
        contact.setFixedSize(contact_size, contact_size)
        contact.setIconSize(QSize(contact_size, contact_size))
        contact.setIcon(QIcon("./icons/contact.svg"))
        contact.move(8, 380)

        #Help button
        help = QPushButton(self)
        help_size = 30
        help.setObjectName("help")
        help.setFixedSize(help_size, help_size)
        help.setIcon(QIcon("./icons/help.svg"))
        help.setIconSize(QSize(help_size, help_size))
        help.move(7, 430)

    def dark(self):
        if self.switch:
            self.setStyleSheet(self.styleSheet().replace("#2E5C6F","#6F2E6C"))
            self.child1.setStyleSheet(self.child1.styleSheet().replace("#DDDDDD","#222222"))
            self.child2.setStyleSheet(self.child2.styleSheet().replace("#2E5C6F","#6F2E6C"))
            self.switch = False
        else:
            self.setStyleSheet(self.styleSheet().replace("#6F2E6C","#2E5C6F"))
            self.child1.setStyleSheet(self.child1.styleSheet().replace("#222222","#DDDDDD"))
            self.child2.setStyleSheet(self.child2.styleSheet().replace("#6F2E6C","#2E5C6F"))
            self.switch = True