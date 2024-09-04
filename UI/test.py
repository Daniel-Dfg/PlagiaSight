from PySide6.QtWidgets import QApplication
from greeting import Greetings

app = QApplication([])
window = Greetings()
window.show()
app.exec()
