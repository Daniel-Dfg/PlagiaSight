from PySide6.QtWidgets import QPushButton, QWidget

w = 410
h = 60
class SButtons(QPushButton):
    """
    - Special button
    """
    def __init__(self, text:str= None, parent:QWidget= None) -> None:
        super().__init__(text, parent)
        self.resize(w, h)
        self.setStyleSheet("""
                           QPushButton{
                               background-color:#5C3D58;
                               border-style:none;
                               border-radius:4;
                               color: white;
                               font-size: 18px;
                           }
                           QPushButton::hover{
                               background-color:#996690;
                           }
                           """)
