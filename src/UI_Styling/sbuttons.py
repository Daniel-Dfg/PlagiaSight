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
                               background-color:qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1,stop: 0 #4F3242,stop: 1 #001A27);
                               border-style:none;
                               border-radius:4;
                               color: white;
                               font-size: 18px;
                           }
                           QPushButton::hover{
                               background-color:qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1,stop: 0 #B75353,stop: 1 #5E1D63);
                           }
                           """)
