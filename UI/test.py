from PySide6.QtWidgets import QApplication
from slabels import SLabels

app = QApplication([])
window = SLabels(text="A set of files between eachother")
window.show()
app.exec()
