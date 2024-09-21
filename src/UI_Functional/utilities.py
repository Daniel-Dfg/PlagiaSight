from nltk.tokenize.api import overridden
from typing_extensions import override
from PySide6.QtWidgets import QComboBox, QTextEdit, QLabel, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QHBoxLayout, QFrame, QCheckBox, QListWidget, QAbstractItemView, QMenu, QListWidgetItem
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QStandardItem, QStandardItemModel, QAction
import os
import webbrowser
from numpy import arange
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

MAX_FILES_AMOUNT = 5 #TODO : find a solution to keep the same value in stacked_widget_elems (might be a bit early for a global constants file)


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
    def __init__(self, step1_widget, max_file_amount=MAX_FILES_AMOUNT):
        super().__init__()
        self.setAcceptDrops(True)
        self.max_file_amount = max_file_amount
        self.step1_widget = step1_widget
        if self.max_file_amount == 1:
            self.min_file_amount = 1
        elif self.max_file_amount == MAX_FILES_AMOUNT:
            self.min_file_amount = 2
        else:
            raise ValueError("Invalid max_file_amount value (not 1 or MAX_FILES_AMOUNT)")

        self.correct_files = []
        self.invalid_files = []

        self.instructions_label = QLabel("Drop your content here...")
        self.status_label = QLabel("Nothing yet dropped.")
        self.warning_label = QLabel("Warning will show up here.")
        self.warning_label.setStyleSheet("color: red;")

        self.correct_files_list = QListWidget()
        self.invalid_files_combo = NonSelectableComboBox()

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.instructions_label)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.correct_files_list)  # To display correct files
        layout.addWidget(self.invalid_files_combo)  # To display invalid files
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        #TODO : make this function cleaner
        files = [url.toLocalFile() for url in e.mimeData().urls()]
        valid_set = set(self.correct_files) #for faster lookups and no duplicates
        for file in files:
            if os.path.isfile(file) and self.is_valid_format_file(file) and file not in valid_set:
                if len(self.correct_files) < self.max_file_amount:
                    self.correct_files.append(file)
                    self.add_file_to_list(file)
                    valid_set.add(file)
                else:
                    self.show_warning("⚠️ Maximum file limit reached!")
            elif os.path.isdir(file):
                self.process_directory(file)
            else:
                if file not in valid_set:
                    self.show_warning(f"⚠️ {file} is not a file in a valid format.")
                else:
                    self.show_warning(f"⚠️ {file} has already been added.")
        self.update_status()

    def is_valid_format_file(self, file_path):
        return file_path.endswith('.txt')

    def process_directory(self, directory_path):
        valid_set = set(self.correct_files)
        valid_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if self.is_valid_format_file(os.path.join(directory_path, f)) and f not in valid_set]

        if valid_files:
            for file in valid_files:
                if len(self.correct_files) >= self.max_file_amount:
                    self.show_warning(f"⚠️ Maximum file limit reached while processing {directory_path}. Won't process files from {file} to {valid_files[-1]}.")
                    break
                self.correct_files.append(file)
                self.add_file_to_list(file)
                valid_set.add(file)
            # Only add invalid files if the directory has valid ones
            self.invalid_files.extend([os.path.join(directory_path, f) for f in os.listdir(directory_path) if not self.is_valid_format_file(os.path.join(directory_path, f))])
            self.update_invalid_file_list()
            self.update_status()

    def add_file_to_list(self, file):
        """Add a file to the correct files list with a 'remove' button."""
        item = QListWidgetItem(self.correct_files_list)

        # Create a widget to hold the file path and remove button
        widget = QWidget()
        layout = QHBoxLayout()

        file_label = QLabel(file)  # Show the file path
        remove_button = QPushButton("✕")  # A cross button to remove the file
        remove_button.setStyleSheet("background: none; border: none; color: red; font-weight: bold;")
        remove_button.setFixedSize(20, 20)
        remove_button.clicked.connect(lambda: self.remove_file(file, item))

        # Initially hide the remove button
        remove_button.setVisible(False)

        # Add the file label and remove button to the layout
        layout.addWidget(file_label)
        layout.addWidget(remove_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        widget.setLayout(layout)

        # Set up event filter to handle hover
        widget.installEventFilter(self)

        # Add the widget to the QListWidgetItem
        item.setSizeHint(widget.sizeHint())
        self.correct_files_list.setItemWidget(item, widget)

    def remove_file(self, file, item):
        self.correct_files.remove(file)
        self.correct_files_list.takeItem(self.correct_files_list.row(item))
        self.update_status()

    def update_invalid_file_list(self):
        """Updates the invalid files combo."""
        self.invalid_files_combo.clear()
        if self.invalid_files:
            self.invalid_files_combo.add_item(f"{len(self.invalid_files)} Invalid file{'s' if len(self.invalid_files) > 1 else ''}:")
            for file in self.invalid_files:
                self.invalid_files_combo.add_item(file)
            self.invalid_files_combo.setVisible(True)
        else:
            self.invalid_files_combo.setVisible(False)

    def update_status(self, last_file_dropped = None):
        """Update the status based on the number of correct files."""
        if self.min_file_amount <= len(self.correct_files) <= self.max_file_amount:
            self.set_ready_status()
        else:
            self.status_label.setStyleSheet("color: white;")
            self.status_label.setText(f"⚠️ {len(self.correct_files)} file{'s' if len(self.correct_files) > 1 else ''} dropped.")
            self.show_warning(f"Please drop at least {self.min_file_amount} valid file{'s' if self.min_file_amount==2 else ''}.")
            self.step1_widget.next_button.setEnabled(False)

    def set_ready_status(self):
        self.status_label.setText("🗸 Ready to analyze 🗸")
        self.status_label.setStyleSheet("color: green;")
        self.step1_widget.next_button.setEnabled(True)

    def show_warning(self, message):
        self.warning_label.setText(message)


    def eventFilter(self, arg__1, arg__2):
        obj, event = arg__1, arg__2
        """Handle hover events to show or hide the remove button."""
        if event.type() == QEvent.Type.Enter:
            # Show the remove button when mouse enters the widget
            remove_button = obj.findChild(QPushButton)
            if remove_button:
                remove_button.setVisible(True) #TODO : find an alternative solution to this
        elif event.type() == QEvent.Type.Leave:
            # Hide the remove button when mouse leaves the widget
            remove_button = obj.findChild(QPushButton)
            if remove_button:
                remove_button.setVisible(False)
        return super().eventFilter(obj, event)


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

class GetInTouchWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Get in touch")

        layout = QVBoxLayout()

        label = QLabel("Bug? Feature request? Commentary? Collab? We're all ears!")
        layout.addWidget(label)

        self.add_contact_info(layout, "Daniel D.", ["Texts similarity computations", "UI (functional)"],
                              Mail="mailto:danieldefoing@gmail.com",
                              GitHub="https://github.com/Daniel-Dfg",
                              Discord="https://discord.com/users/720963652286414909")

        self.add_contact_info(layout, "LUCKYINS", ["Web scraping", "UI (styling)"],
                              GitHub="https://github.com/Luckyyyin")

        self.add_contact_info(layout, "onuriscoding", ["UX Design", "GitHub workflows"],
                              GitHub="https://github.com/onuriscoding")

        self.add_contact_info(layout, "botEkrem", ["General Consultancy", "GitHub workflows", "Cross-platform compatibility (dockerization)"],
                              GitHub="https://github.com/BotEkrem")

        self.setLayout(layout)

    def add_contact_info(self, parent_layout, name, roles=[], *args, **kwargs):
        if len(kwargs) > 3 or not kwargs:
            raise ValueError("Too many/few contacts (1 to 3)")

        contact_widget = QWidget()
        contact_layout = QVBoxLayout()

        contact_header = QWidget()
        contact_header_layout = QHBoxLayout()

        contact_label = QLabel(name + ": ")
        contact_header_layout.addWidget(contact_label)

        all_socials = sorted(kwargs.keys())
        for social in all_socials:
            button = QPushButton()
            button.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{social}_icon.png"))
            button.setToolTip(social)
            button.clicked.connect(lambda _, link=kwargs[social]: webbrowser.open(link))
            contact_header_layout.addWidget(button)

        contact_header.setLayout(contact_header_layout)
        contact_layout.addWidget(contact_header)

        toggle_checkbox = QCheckBox("Show roles")
        roles_widget = QWidget()
        roles_layout = QVBoxLayout()

        for role in roles:
            role_label = QLabel(f"• {role}")
            roles_layout.addWidget(role_label)

        roles_widget.setLayout(roles_layout)
        roles_widget.setVisible(False)

        toggle_checkbox.toggled.connect(lambda checked: self.toggle_roles(roles_widget, toggle_checkbox, checked))

        contact_layout.addWidget(toggle_checkbox)
        contact_layout.addWidget(roles_widget)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        contact_layout.addWidget(separator)

        contact_widget.setLayout(contact_layout)
        parent_layout.addWidget(contact_widget)

    def toggle_roles(self, roles_widget, toggle_checkbox, checked):
        if checked:
            toggle_checkbox.setText("Hide roles")
            roles_widget.setVisible(True)
        else:
            toggle_checkbox.setText("Show roles")
            roles_widget.setVisible(False)

class GraphWindow(QWidget):
    #TODO : documentation of this
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.setWindowTitle("Graphs: Sentence Length & Word Frequencies")
        layout = QVBoxLayout(self)

        button_layout = QHBoxLayout()
        self.previous_button = QPushButton("Previous Graph")
        self.previous_button.clicked.connect(self.show_previous_graph)
        self.next_button = QPushButton("Next Graph")
        self.next_button.clicked.connect(self.show_next_graph)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)

        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

        # Initialisation de l'axe pour les graphiques
        self._static_ax = self.canvas.figure.subplots()

        # Liste des noms des graphiques ajoutés
        self.graph_names = []
        self.current_graph_index = 0

    def add_graph(self, name, freq_dist1, freq_dist2, x_label, y_label, title):
        """
        Generic method to add a comparison graph from a FreqDist distribution.
        """
        all_keys = set(freq_dist1.keys()).union(set(freq_dist2.keys()))

        total_frequencies = {key: freq_dist1.get(key, 0) + freq_dist2.get(key, 0) for key in all_keys}

        sorted_keys = sorted(total_frequencies.keys(), key=lambda k: total_frequencies[k], reverse=True)

        threshold_percentage = 0.1  # 10% of terms kept if...
        threshold = 30 # ... more than 30 terms in total
        if len(sorted_keys) > threshold:
            sorted_keys = sorted_keys[:int(len(sorted_keys) * threshold_percentage)]

        y_data1 = [freq_dist1.get(key, 0) for key in sorted_keys]
        y_data2 = [freq_dist2.get(key, 0) for key in sorted_keys]

        # Prepare graph data
        graph_data = (sorted_keys, y_data1, y_data2, x_label, y_label, title)
        setattr(self, name, graph_data)
        self.graph_names.append(name)
        self.current_graph_index = len(self.graph_names) - 1
        self.show_graph(name)

    def update_graph(self, name, freq_dist1, freq_dist2, x_label, y_label, title):
        if hasattr(self, name):
            common_keys = list(set(freq_dist1.keys()).intersection(set(freq_dist2.keys())))
            common_keys.sort()

            y_data1 = [freq_dist1[key] for key in common_keys]
            y_data2 = [freq_dist2[key] for key in common_keys]

            graph_data = (common_keys, y_data1, y_data2, x_label, y_label, title)
            setattr(self, name, graph_data)
            if self.graph_names[self.current_graph_index] == name:
                self.show_graph(name)
        else:
            raise AttributeError(f"No graph named '{name}' found.")

    def show_graph(self, name):
        #TODO : document this
        if hasattr(self, name):
            self._static_ax.clear()
            x_data, y_data1, y_data2, x_label, y_label, title = getattr(self, name)
            bar_width = 0.35
            index = arange(len(x_data))
            self._static_ax.bar(index, y_data1, bar_width, label='Text 1')
            self._static_ax.bar(index + bar_width, y_data2, bar_width, label='Text 2')

            self._static_ax.set_xlabel(x_label)
            self._static_ax.set_ylabel(y_label)
            self._static_ax.set_title(title)
            self._static_ax.set_xticks(index + bar_width / 2)
            self._static_ax.set_xticklabels(x_data, rotation=45, ha="right")
            self._static_ax.legend()
            self.canvas.draw()
        else:
            raise AttributeError(f"No graph named '{name}' found.")

    def show_previous_graph(self):
        if self.current_graph_index > 0:
            self.current_graph_index -= 1
        else:
            self.current_graph_index = len(self.graph_names) - 1
        self.show_graph(self.graph_names[self.current_graph_index])

    def show_next_graph(self):
        if self.current_graph_index < len(self.graph_names) - 1:
            self.current_graph_index += 1
        else:
            self.current_graph_index = 0
        self.show_graph(self.graph_names[self.current_graph_index])
