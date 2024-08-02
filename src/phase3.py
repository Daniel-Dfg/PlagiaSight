from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QToolBar, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
import webbrowser
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plagialand")

        # Layout principal
        main_layout = QVBoxLayout()

        # Section de bienvenue
        welcome_label = QLabel("#1 : Welcoming message\nI want to compare...")
        main_layout.addWidget(welcome_label)

        # Boutons de choix
        button1 = QPushButton("One file with related online data")
        main_layout.addWidget(button1)

        button2 = QPushButton("Several files between eachother")
        button2.setToolTip("Useful for a highschool class, for instance (max N files)")
        main_layout.addWidget(button2)

        # Conteneur pour le layout principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Barre d'outils en bas

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(Qt.BottomToolBarArea, toolbar)


        # Boutons de la barre d'outils
        # Widget pour centrer les actions
        center_widget = QWidget()
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_widget.setLayout(center_layout)

        # Actions avec icônes et hyperliens
        action_contact_dev = QAction(QIcon("path/to/contact_icon.png"), "", self)
        action_contact_dev.triggered.connect(webbrowser.open("mailto:danieldefoing@gmail.com"))

        center_layout.addWidget(toolbar.addAction(action_contact_dev))

        action_view_github = QAction(QIcon("path/to/github_icon.png"), "", self)
        action_view_github.triggered.connect(lambda: self.open_url("https://github.com/your-repo"))
        center_layout.addWidget(toolbar.addAction(action_view_github))

        action_help = QAction(QIcon("path/to/help_icon.png"), "", self)
        action_help.triggered.connect(lambda: self.open_url("path/to/help.html"))
        center_layout.addWidget(toolbar.addAction(action_help))

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
