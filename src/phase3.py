from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSpacerItem, QSizePolicy, QTreeWidgetItem, QTreeWidget, QStackedWidget, QTextEdit, QFileDialog, QComboBox, QListWidget, QRadioButton, QButtonGroup
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent, QStandardItem, QStandardItemModel
import webbrowser
import os

CLASSIC_STYLESHEET = """
color: black;
background-color: white;
"""

class NonSelectableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.standard_model = QStandardItemModel(self)
        self.setModel(self.standard_model)

    def add_item(self, text, selectable=False):
        item = QStandardItem(text)
        if not selectable:
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
        self.standard_model.appendRow(item)

class DropArea(QTextEdit):
    def __init__(self, expected_type, step1_widget):
        super().__init__()
        self.setAcceptDrops(True)
        self.expected_type = expected_type
        self.step1_widget = step1_widget
        self.warning_label = QLabel("No content dropped yet.")
        self.warning_label.setStyleSheet("color: yellow;")
        self.correct_files = []
        self.invalid_files = []

        self.invalid_files_combo = NonSelectableComboBox()
        self.invalid_files_combo.setVisible(False)

        if self.expected_type == "file":
            self.setText("Drop a .txt file here or click 'Browse'")
        elif self.expected_type == "directory":
            self.setText("Drop a directory with .txt files here or click 'Browse'")

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        self.invalid_files = []
        files = [url.toLocalFile() for url in e.mimeData().urls()]
        if self.expected_type == "file":
            if len(files) == 1 and os.path.isfile(files[0]):
                if self.is_valid_format_file(files[0]):
                    self.setText(self.simplify_path(files[0]))
                    self.set_ready_status()
                    self.correct_files = [files[0]]
                else:
                    self.show_warning("Please drop only .txt files.")
            else:
                self.show_warning("Please drop only one file.")
        elif self.expected_type == "directory":
            if len(files) == 1 and os.path.isdir(files[0]):
                self.process_directory(files[0])
            else:
                self.show_warning("Please drop only one directory.")

    def is_valid_format_file(self, file_path):
        return file_path.endswith('.txt')

    def process_directory(self, directory_path):
        self.correct_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if self.is_valid_format_file(os.path.join(directory_path, f))]
        self.invalid_files = [f for f in os.listdir(directory_path) if not self.is_valid_format_file(os.path.join(directory_path, f))]
        self.show_warning(f"{len(self.invalid_files)} invalid files found.")
        self.show_invalid_files()
        self.show_correct_files()
        self.check_valid_directory()

    def simplify_path(self, full_path):
        return os.path.join(".../", os.path.basename(os.path.dirname(full_path)), os.path.basename(full_path))

    def show_warning(self, message):
        self.warning_label.setText(message)
        self.warning_label.setStyleSheet("color: red;")

    def set_ready_status(self):
        self.warning_label.setText("Ready to analyze.")
        self.warning_label.setStyleSheet("color: green;")
        self.step1_widget.next_button.setEnabled(True)

    def show_invalid_files(self):
        self.invalid_files_combo.clear()
        self.invalid_files_combo.add_item(f"{len(self.invalid_files)} Invalid file{'s' if len(self.invalid_files) > 1 else ""}:", selectable=True)
        for f in self.invalid_files:
            self.invalid_files_combo.add_item(f)
        self.invalid_files_combo.setVisible(True)

    def show_correct_files(self):
        self.step1_widget.correct_files_list.clear()
        self.step1_widget.correct_files_list.addItems(self.correct_files)
        self.step1_widget.correct_files_list.setVisible(True)

    def check_valid_directory(self):
        if 2 <= len(self.correct_files) <= 5:
            self.set_ready_status()
        else:
            self.show_warning("Please select a directory with 2 to 5 .txt files.")
            self.step1_widget.next_button.setEnabled(False)

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
        self.main_window.help_window.expand_step(1)

class Step1Widget(QWidget):
    def __init__(self, main_window, expected_type):
        super().__init__()
        self.main_window = main_window
        self.expected_type = expected_type

        layout = QVBoxLayout()

        self.label = QLabel("Drop your files or directories below or click 'Browse':")
        layout.addWidget(self.label)

        warning_layout = QVBoxLayout()
        self.warning_label = QLabel("")
        warning_layout.addWidget(self.warning_label)

        self.drop_area = DropArea(expected_type, self)
        layout.addWidget(self.drop_area)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.browse_button)

        layout.addWidget(self.drop_area.warning_label)
        layout.addWidget(self.drop_area.invalid_files_combo)

        self.correct_files_list = QListWidget()
        self.correct_files_list.setVisible(False)
        layout.addWidget(self.correct_files_list)

        layout.addLayout(warning_layout)

        back_and_next = QHBoxLayout()
        back_and_next_widget = QWidget()

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        back_and_next.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.proceed_to_step2)
        back_and_next.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        back_and_next_widget.setLayout(back_and_next)
        layout.addWidget(back_and_next_widget)
        self.setLayout(layout)

    def go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(0)
        self.main_window.help_window.expand_step(0)

    def open_file_dialog(self):
        if self.expected_type == "file":
            file_name, _ = QFileDialog.getOpenFileName(self, "Select a .txt file", "", "Text Files (*.txt)")
            if file_name:
                if self.drop_area.is_valid_format_file(file_name):
                    self.drop_area.setText(self.drop_area.simplify_path(file_name))
                    self.drop_area.set_ready_status()
                    self.drop_area.correct_files = [file_name]
                    self.next_button.setEnabled(True)
                else:
                    self.drop_area.show_warning("Please select only .txt files.")
                    self.next_button.setEnabled(False)
        elif self.expected_type == "directory":
            directory_path = QFileDialog.getExistingDirectory(self, "Select a directory with .txt files")
            if directory_path:
                self.drop_area.process_directory(directory_path)

    def proceed_to_step2(self):
        print("Proceeding to step 2 with files:", self.drop_area.correct_files)
        self.main_window.step2_widget = Step2Widget(self.main_window)
        self.main_window.stacked_widget.addWidget(self.main_window.step2_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step2_widget)
        self.main_window.help_window.expand_step(2)


class HelpWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Help")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree)

        self.add_help_step("Step 0: Welcome", "This is the welcoming message.\nYou can compare files and more.")
        self.add_help_step("Step 1: Select Comparison Type", "Choose whether you want to compare a single file with online data or multiple files.")
        self.add_help_step("Step 2: Choose Analysis Type", "Select whether you want a simple or complex analysis of your files.")
        self.setLayout(layout)

    def add_help_step(self, step_title, step_details):
        step_item = QTreeWidgetItem([step_title])
        self.tree.addTopLevelItem(step_item)

        details_item = QTreeWidgetItem([step_details])
        step_item.addChild(details_item)

        step_item.setExpanded(False)

    def expand_step(self, step_index):
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            item.setExpanded(i == step_index)

class Step2Widget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        self.label = QLabel("Choose the type of analysis you want to perform:")
        layout.addWidget(self.label)

        self.simple_analysis_radio = QRadioButton("Simple Analysis")
        self.complex_analysis_radio = QRadioButton("Complex Analysis")

        self.analysis_group = QButtonGroup()
        self.analysis_group.addButton(self.simple_analysis_radio)
        self.analysis_group.addButton(self.complex_analysis_radio)

        layout.addWidget(self.simple_analysis_radio)
        layout.addWidget(self.complex_analysis_radio)

        self.description_label = QLabel("Select an analysis type to see a brief description.")
        layout.addWidget(self.description_label)

        self.launch_button = QPushButton("LAUNCH")
        self.launch_button.setEnabled(False)
        self.launch_button.clicked.connect(self.launch_analysis)
        layout.addWidget(self.launch_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.simple_analysis_radio.toggled.connect(self.update_description)
        self.complex_analysis_radio.toggled.connect(self.update_description)

        self.setLayout(layout)

    def update_description(self):
        if self.simple_analysis_radio.isChecked():
            self.description_label.setText("Simple Analysis: A quick overview of the files.")
            self.launch_button.setEnabled(True)
        elif self.complex_analysis_radio.isChecked():
            self.description_label.setText("Complex Analysis: A detailed and thorough analysis.")
            self.launch_button.setEnabled(True)

    def launch_analysis(self):
        selected_analysis = "Simple" if self.simple_analysis_radio.isChecked() else "Complex"
        print(f"Launching {selected_analysis} Analysis")
        # Implement the logic to launch the selected analysis


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plagialand")

        self.main_layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()

        self.step0_widget = Step0Widget(self)
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

class GetInTouchWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Get in touch")

        layout = QVBoxLayout()

        label = QLabel("Bug? Feature request? Commentary? Collab? We're all ears!")
        layout.addWidget(label)

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

        contact_label = QLabel(name + ": ")
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
