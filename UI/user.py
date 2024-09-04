from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QWidget, QFrame, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer

rec_size = (45, 480)
class UserInfo(QFrame):
    def __init__(self, parent: QWidget= None) -> None:
        super().__init__(parent)
        
        #UserInfo
        self.setFixedSize(rec_size[0], rec_size[1])
        self.setStyleSheet("""
                           *{
                               background-color:#2E5C6F;
                               border-style:none;
                           }
                           QFrame{
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
        shadow.setColor(QColor("black"))
        self.setGraphicsEffect(shadow)
        
        #Up
        #Setting
        setting = QPushButton(self)
        setting_size= 30
        setting.setObjectName("setting")
        setting.setFixedSize(setting_size, setting_size)
        setting.setIcon(QIcon("./icons/setting.svg"))
        setting.setIconSize(QSize(setting_size, setting_size))
        setting.setGeometry(7, 60, 0, 0)
        
        #Wifi
        wifi = QPushButton(self)
        wifi_size= 30
        wifi.setObjectName("wifi")
        wifi.setFixedSize(wifi_size, wifi_size)
        wifi.setIcon(QIcon("./icons/wifi.svg"))
        wifi.setIconSize(QSize(wifi_size, wifi_size))
        wifi.setGeometry(8, 100, 0, 0)
        
        #Down
        #DarkMode
        dark_mode = QPushButton(self)
        dark_mode_size = 35
        dark_mode.setObjectName("dark_mode")
        dark_mode.setFixedSize(dark_mode_size, dark_mode_size)
        dark_mode.setIconSize(QSize(dark_mode_size, dark_mode_size))
        dark_mode.setIcon(QIcon("./icons/darkmode.svg"))
        dark_mode.setGeometry(4, 330, 0, 0)
        
        #Contact button
        contact = QPushButton(self)
        contact_size = 28
        contact.setObjectName("contact")
        contact.setFixedSize(contact_size, contact_size)
        contact.setIconSize(QSize(contact_size, contact_size))
        contact.setIcon(QIcon("./icons/contact.svg"))
        contact.setGeometry(8, 380, 0, 0)
        
        #Help button
        help = QPushButton(self)
        help_size = 30
        help.setObjectName("help")
        help.setFixedSize(help_size, help_size)
        help.setIcon(QIcon("./icons/help.svg"))
        help.setIconSize(QSize(help_size, help_size))
        help.setGeometry(7, 430, 0, 0)
        
        
   