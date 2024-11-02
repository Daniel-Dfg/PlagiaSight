from PySide6.QtWidgets import QStackedWidget, QVBoxLayout
from .stacked_widget_elems import Step0_WelcomingMessage
from .utilities import GetInTouchWindow, HelpWindow
from PySide6.QtCore import Qt, QTimer
import webbrowser
from UI_Styling import smainwindow, stitlebar, userTools


class MainWindow(smainwindow.SMainWindow):
    def __init__(self):
        super().__init__()
        #Main Layout
        self.setWindowTitle("PlagiaSight")

        self.stacked_widget = QStackedWidget()
        self.step0_widget = Step0_WelcomingMessage(self)
        self.stacked_widget.addWidget(self.step0_widget)
        self.main_layout.addWidget(self.stacked_widget)

        self.usertools = userTools.UserTools(self)

        # Buttons tooltip + functions
        buttons = {self.usertools.contact: ("Get in touch",self.toggle_GetInTouchWindow),
            self.usertools.help:("Help", self.toggle_HelpWindow),
            self.usertools.setting: ("View project on GitHub", lambda: webbrowser.open("https://github.com/LUCKYINS/PlagiarismDetectionProject"))}

        # Set Buttons
        for button,func in buttons.items():
            button.setToolTip(func[0])
            button.clicked.connect(func[1])

        self.main_layout.addWidget(self.usertools, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        # Load stuff in the background
        QTimer.singleShot(180, self.init_sub_windows)

    def init_sub_windows(self):
        self.get_in_touch_window = GetInTouchWindow(self)
        self.help_window = HelpWindow()
        self.get_in_touch_window.full_init()

    def toggle_GetInTouchWindow(self):
        if self.get_in_touch_window is not None:
            if not self.get_in_touch_window.is_fully_init:
                self.get_in_touch_window.full_init()
            if self.get_in_touch_window.isVisible():
                self.get_in_touch_window.hide()
            else:
                self.get_in_touch_window.show()

    def toggle_HelpWindow(self):
        if self.help_window is not None:
            if self.help_window.isVisible():
                self.help_window.hide()
            else:
                self.help_window.show()
                current_index = self.stacked_widget.currentIndex()
                self.help_window.expand_step(current_index)
