from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSpacerItem, QSizePolicy, QTreeWidgetItem, QTreeWidget, QStackedWidget, QTextEdit, QMessageBox
from PySide6.QtCore import Qt, QEvent, QUrl
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent
import webbrowser
import os

class DropArea(QTextEdit):
    def __init__(self, expected_type, warning_label):
        super().__init__()
        self.setAcceptDrops(True)
        self.expected_type = expected_type
        self.warning_label = warning_label
        self.update_text()

    def update_text(self):
        if self.expected_type == "file":
            self.setText("Drop files here")
        elif self.expected_type == "directory":
            self.setText("Drop directories here")

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        self.warning_label.setText("")
        files = [url.toLocalFile() for url in e.mimeData().urls()]
        if self.expected_type == "file":
            if all(os.path.isfile(f) for f in files):
                self.setText("\n".join(files))
            else:
                self.show_warning("Please drop only files.")
        elif self.expected_type == "directory":
            if all(os.path.isdir(f) for f in files):
                self.setText("\n".join(files))
            else:
                self.show_warning("Please drop only directories.")
        else:
            self.show_warning("Invalid input type.")

    def show_warning(self, message):
        self.warning_label.setText(message)
        self.warning_label.setStyleSheet("color: red;")

class Step0Widget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        welcome_label = QLabel("#0: Welcoming message\nI want to compare...")
        layout.addWidget(welcome_label)

        button1 = QPushButton("One file with related online data")
        button1.clicked.connect(lambda: self.proceed_to_step1("file"))
        layout.addWidget(button1)

        button2 = QPushButton("Several files between each other")
        button2.setToolTip("Useful for a high school class, for instance (max N files)")
        button2.clicked.connect(lambda: self.proceed_to_step1("directory"))
        layout.addWidget(button2)

        self.setLayout(layout)

    def proceed_to_step1(self, expected_type):
        self.main_window.step1_widget = Step1Widget(self.main_window, expected_type)
        self.main_window.stacked_widget.addWidget(self.main_window.step1_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step1_widget)

class Step1Widget(QWidget):
    def __init__(self, main_window, expected_type):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        self.label = QLabel("Drop your files or directories below:")
        layout.addWidget(self.label)

        self.warning_label = QLabel("")
        layout.addWidget(self.warning_label)

        self.drop_area = DropArea(expected_type, self.warning_label)
        layout.addWidget(self.drop_area)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

    def go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(0)

class HelpWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Help")
        self.resize(400, 300)

        layout = QVBoxLayout()

        # Ajouter la QTreeWidget pour les étapes d'aide
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # Cache l'en-tête
        layout.addWidget(self.tree)

        # Ajouter des étapes et leurs explications
        self.add_help_step("Step 0: Welcome", "This is the welcoming message.\nYou can compare files and more.")
        self.add_help_step("Step 1: Select Comparison Type", "Choose whether you want to compare a single file with online data or multiple files.")
        self.add_help_step("Step 2: Get Results", "View the results of the plagiarism check.")

        self.setLayout(layout)

    def add_help_step(self, step_title, step_details):
        # Crée un item de la QTreeWidget pour l'étape
        step_item = QTreeWidgetItem([step_title])
        self.tree.addTopLevelItem(step_item)

        # Crée un item enfant pour les détails de l'étape
        details_item = QTreeWidgetItem([step_details])
        step_item.addChild(details_item)

        # Masque les détails par défaut
        step_item.setExpanded(False)

    def expand_step(self, step_index):
        top_level_item = self.tree.topLevelItem(step_index)
        if top_level_item:
            top_level_item.setExpanded(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plagialand")

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Créer le QStackedWidget pour gérer les différentes étapes
        self.stacked_widget = QStackedWidget()

        # Ajouter les widgets des différentes étapes
        self.step0_widget = Step0Widget(self)
        self.stacked_widget.addWidget(self.step0_widget)

        self.main_layout.addWidget(self.stacked_widget)

        # Créer les fenêtres de "Get In Touch" et "Help"
        self.get_in_touch_window = GetInTouchWindow(self)
        self.help_window = HelpWindow(self)

        # Boutons d'actions
        bottom_bar_layout = QHBoxLayout()
        action_contact_dev = QPushButton()
        action_contact_dev.setToolTip("Get in touch")
        action_contact_dev.setIcon(QIcon("Resources/Excess Files/UI_elements/get-in-touch-icon-34.png"))
        action_contact_dev.clicked.connect(self.toggle_GetInTouchWindow)

        action_view_github = QPushButton()
        action_view_github.setToolTip("View the project on GitHub")
        action_view_github.setIcon(QIcon("Resources/Excess Files/UI_elements/github_icon.png"))
        action_view_github.clicked.connect(lambda: webbrowser.open("https://github.com/Luckyyyin/PlagiarismDetectionProject"))

        action_help = QPushButton()
        action_help.setToolTip("Help")
        action_help.setIcon(QIcon("Resources/Excess Files/UI_elements/help_icon.png"))
        action_help.clicked.connect(self.toggle_HelpWindow)

        # Ajouter les boutons et les espacements
        bottom_bar_layout.addWidget(action_contact_dev)
        bottom_bar_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_bar_layout.addWidget(action_view_github)
        bottom_bar_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_bar_layout.addWidget(action_help)

        self.main_layout.addLayout(bottom_bar_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def toggle_GetInTouchWindow(self):
        if self.get_in_touch_window.isVisible():
            self.get_in_touch_window.hide()
        else:
            self.get_in_touch_window.show()

    def toggle_HelpWindow(self):
        if self.help_window.isVisible():
            self.help_window.hide()
        else:
            self.help_window.show()

class GetInTouchWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

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
        if len(kwargs) > 3 or not kwargs:
            raise ValueError("Too many/few contacts (1 to 3)")

        contact_widget = QWidget()
        contact_layout = QHBoxLayout()

        contact_label = QLabel(name + " : ")
        contact_layout.addWidget(contact_label)

        all_socials = sorted(kwargs.keys())
        social_button_1 = QPushButton()
        social_button_1.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{all_socials[0]}_icon.png"))
        social_button_1.setToolTip(all_socials[0])
        social_button_1.clicked.connect(lambda: webbrowser.open(kwargs[all_socials[0]]))
        contact_layout.addWidget(social_button_1)

        if len(all_socials) > 1:
            social_button_2 = QPushButton()
            social_button_2.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{all_socials[1]}_icon.png"))
            social_button_2.setToolTip(all_socials[1])
            social_button_2.clicked.connect(lambda: webbrowser.open(kwargs[all_socials[1]]))
            contact_layout.addWidget(social_button_2)

        if len(all_socials) > 2:
            social_button_3 = QPushButton()
            social_button_3.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{all_socials[2]}_icon.png"))
            social_button_3.setToolTip(all_socials[2])
            social_button_3.clicked.connect(lambda: webbrowser.open(kwargs[all_socials[2]]))
            contact_layout.addWidget(social_button_3)

        contact_widget.setLayout(contact_layout)
        parent_layout.addWidget(contact_widget)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
