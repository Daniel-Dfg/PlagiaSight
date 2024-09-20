from PySide6.QtWidgets import QPushButton, QWidget

w = 410
h = 60
class SButtons(QPushButton):
    """
    - Special button
    """
    def __init__(self, text:str, parent:QWidget= None) -> None:
        super().__init__(text, parent)
        self.resize(w, h)
        self.setStyleSheet("""
                           *{
                               background-color:#5E485A;
                               border-style:none;
                               border-radius:4;
                               color: white;
                               font-size: 18px;
                           }
                           """)
