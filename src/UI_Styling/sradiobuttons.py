from PySide6.QtWidgets import QRadioButton

class SRadioButton(QRadioButton):
    def __init__(self, text:str= None) -> None:
        super().__init__(text)
        self.setStyleSheet("""
            *{
                font-size: 20px;
            }
            QRadioButton::indicator {
                    width: 40px;
                    height: 40px;
                    border-radius: 5px;
                    background-color: rgba(255, 255, 255, 25);
                }
            QRadioButton::indicator:checked {
                    background-color: rgba(255, 200, 200, 100);
                }
            """)
