from PySide6.QtWidgets import QComboBox, QTextEdit, QLabel, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QStandardItem, QStandardItemModel
import os
import webbrowser
from numpy import arange
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


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
        self.warning_label.setStyleSheet("color: white;")
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
        #TODO : separate warning and status labels by making a new one for warnings only
        self.invalid_files = []
        files = [url.toLocalFile() for url in e.mimeData().urls()]
        if self.expected_type == "file":
            if len(files) == 1 and os.path.isfile(files[0]):
                if self.is_valid_format_file(files[0]):
                    self.setText(self.simplify_path(files[0]))
                    self.set_ready_status()
                    self.correct_files = [files[0]]
                else:
                    self.show_warning("⚠️ Please drop only .txt files.")
            else:
                self.show_warning("⚠️ Please drop only one file.")
        elif self.expected_type == "directory":
            if len(files) == 1 and os.path.isdir(files[0]):
                self.process_directory(files[0])
            else:
                self.show_warning("⚠️ Please drop only one directory.")

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
        self.warning_label.setText("🗸 Ready to analyze 🗸")
        self.warning_label.setStyleSheet("color: green;")
        self.step1_widget.next_button.setEnabled(True)

    def show_invalid_files(self):
        self.invalid_files_combo.clear()
        self.invalid_files_combo.add_item(f"{len(self.invalid_files)} Invalid file{'s' if len(self.invalid_files) > 1 else ''}:", selectable=True)
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

        self.add_contact_info(layout, "Daniel D.", Mail="mailto:danieldefoing@gmail.com",
                              GitHub="https://github.com/Daniel-Dfg",
                              Discord="https://discord.com/users/720963652286414909")

        self.add_contact_info(layout, "LUCKYINS", GitHub="https://github.com/Luckyyyin")
        self.add_contact_info(layout, "onuriscoding", GitHub="https://github.com/onuriscoding")

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

        #TODO : add a section below with each person's roles in the project, so customers know
        #who to contact immmediately.
        contact_widget.setLayout(contact_layout)
        parent_layout.addWidget(contact_widget)

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
