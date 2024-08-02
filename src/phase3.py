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

        button_layout = QHBoxLayout()
        button_widget = QWidget()
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_widget = QWidget()
        # Section de bienvenue
        welcome_label = QLabel("#1 : Welcoming message\nI want to compare...")

        # Boutons de choix
        button1 = QPushButton("One file with related online data")
        button_layout.addWidget(button1)

        button2 = QPushButton("Several files between eachother")
        button2.setToolTip("Useful for a highschool class, for instance (max N files)")
        button_layout.addWidget(button2)
        button_widget.setLayout(button_layout)

        bottom_bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        bottom_bar_widget.setLayout(bottom_bar_layout)

        self.get_in_touch_window = None
        # Actions avec icônes et hyperliens
        action_contact_dev = QPushButton()
        action_contact_dev.setToolTip("Get in touch")
        action_contact_dev.setIcon(QIcon("Resources/Excess Files/UI_elements/get-in-touch-icon-34.png"))
        action_contact_dev.clicked.connect(lambda : self.open_GetInTouchWindow())
        bottom_bar_layout.addWidget(action_contact_dev)

        action_view_github = QPushButton()
        action_view_github.setToolTip("View the project on GitHub")
        action_view_github.setIcon(QIcon("Resources/Excess Files/UI_elements/github_icon.png"))
        action_view_github.clicked.connect(lambda : webbrowser.open("https://github.com"))

        #action_help = QAction(QIcon("path/to/help_icon.png"), "", self)
        #action_help.triggered.connect(...)

        main_layout.addWidget(welcome_label)
        main_layout.addWidget(button_widget)
        main_layout.addWidget(bottom_bar_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_GetInTouchWindow(self):
        self.get_in_touch_window = GetInTouchWindow()
        self.get_in_touch_window.show()


class GetInTouchWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Get in touch")

        layout = QVBoxLayout()

        label = QLabel("Bug ? Feature request ? Commentary ? Collab ? We're all ears !")
        layout.addWidget(label)

        # Ajouter les contacts
        self.add_contact_info(layout, "Daniel D.", Mail="mailto:danieldefoing@gmail.com",
                                GitHub="https://github.com/Daniel-Dfg",
                                Discord="https://discord.com/users/720963652286414909")

        self.add_contact_info(layout, "Luckyyyin", GitHub="https://github.com/Luckyyyin")

        self.setLayout(layout)

    def add_contact_info(self, parent_layout, name, *args, **kwargs):
        #max 3 contacts
        if len(kwargs) > 3 or not kwargs:
            raise ValueError("Too many/few contacts (1 to 3)")

        contact_widget = QWidget()
        contact_layout = QHBoxLayout()

        contact_label = QLabel(name + " : ")
        contact_layout.addWidget(contact_label)

        all_socials = sorted(kwargs.keys())
        social_button_1 = QPushButton(all_socials[0])
        social_button_1.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{all_socials[0]}_icon.png"))
        social_button_1.clicked.connect(lambda: webbrowser.open(kwargs[all_socials[0]]))
        contact_layout.addWidget(social_button_1)

        if len(all_socials) > 1:
            social_button_2 = QPushButton(all_socials[1])
            social_button_2.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{all_socials[1]}_icon.png"))
            social_button_2.clicked.connect(lambda: webbrowser.open(kwargs[all_socials[1]]))
            contact_layout.addWidget(social_button_2)

        if len(all_socials) > 2:
            social_button_3 = QPushButton(all_socials[2])
            social_button_3.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{all_socials[2]}_icon.png"))
            social_button_3.clicked.connect(lambda: webbrowser.open(kwargs[all_socials[2]]))
            contact_layout.addWidget(social_button_3)

        #for social in kwargs:
            # align left, fix size, etc. #TODO

        contact_widget.setLayout(contact_layout)
        parent_layout.addWidget(contact_widget)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
