from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QStackedWidget, QPushButton, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QApplication
from PySide6.QtGui import QIcon
from .stacked_widget_elems import Step0_WelcomingMessage
from .utilities import GetInTouchWindow, HelpWindow
import webbrowser

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plagialand")

        self.main_layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()

        self.step0_widget = Step0_WelcomingMessage(self)
        self.stacked_widget.addWidget(self.step0_widget)

        self.main_layout.addWidget(self.stacked_widget)

        self.get_in_touch_window = GetInTouchWindow(self)
        self.help_window = HelpWindow(self)

        bottom_bar_layout = QHBoxLayout()
        action_contact_dev = QPushButton()
        action_contact_dev.setToolTip("Get in touch")
        action_contact_dev.setIcon(QIcon("Resources/Excess Files/UI_elements/contact_dev_icon-34.png"))
        action_contact_dev.clicked.connect(self.toggle_GetInTouchWindow)

        action_view_github = QPushButton()
        action_view_github.setToolTip("View project on GitHub")
        action_view_github.setIcon(QIcon("Resources/Excess Files/UI_elements/github-icon-34.png"))
        action_view_github.clicked.connect(lambda: webbrowser.open("https://github.com/Luckyyyin/Plagialand"))

        action_help = QPushButton()
        action_help.setToolTip("Help")
        action_help.setIcon(QIcon("Resources/Excess Files/UI_elements/help-icon-34.png"))
        action_help.clicked.connect(self.toggle_HelpWindow)

        bottom_bar_layout.addWidget(action_contact_dev)
        bottom_bar_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        bottom_bar_layout.addWidget(action_view_github)
        bottom_bar_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        bottom_bar_layout.addWidget(action_help)

        bottom_bar = QWidget()
        bottom_bar.setLayout(bottom_bar_layout)

        self.main_layout.addWidget(bottom_bar)
        self.main_layout.addStretch(1)

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)


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
            current_index = self.stacked_widget.currentIndex()
            self.help_window.expand_step(current_index)
