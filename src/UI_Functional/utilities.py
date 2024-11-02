from matplotlib.backends.backend_agg import RendererAgg
from nltk.probability import SimpleGoodTuringProbDist
from nltk.tokenize.api import overridden
from typing_extensions import override
from PySide6.QtWidgets import QComboBox, QTextEdit, QLabel, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QFrame, QCheckBox, QListWidget, QAbstractItemView, QMenu, QListWidgetItem
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont, QIcon, QPainter, QStandardItem, QStandardItemModel, QAction, QColor
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
import os
import webbrowser
from numpy import arange

from UI_Styling.sdroparea import SDropArea
from UI_Styling.smainwindow import SMainWindow
from UI_Styling.sminiwindow import SMiniWindow
from UI_Styling.sbuttons import SButtons

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


class DropArea(SDropArea):
    def __init__(self, step1_widget, max_file_amount=5):
        super().__init__()
        self.setAcceptDrops(True)
        self.max_file_amount = max_file_amount
        self.step1_widget = step1_widget

        # Limite minimum de fichiers
        self.min_file_amount = 1 if max_file_amount == 1 else 2

        self.correct_files = []
        self.invalid_files = []

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        files = [url.toLocalFile() for url in e.mimeData().urls()]
        valid_set = set(self.correct_files)
        for file in files:
            if os.path.isfile(file) and self.file_format_is_valid(file) and file not in valid_set:
                if len(self.correct_files) < self.max_file_amount:
                    self.correct_files.append(file)
                    self.step1_widget.add_file_to_correct_files_list_UI(file,True)
                    valid_set.add(file)
                else:
                    self.step1_widget.show_warning("⚠️ Maximum file limit reached!")
            elif os.path.isdir(file):
                self.process_directory(file)
            else:
                if file not in valid_set:
                    self.step1_widget.show_warning(f"⚠️ .{file.split('.')[-1]} is not a valid file format.")
        self.step1_widget.update_current_content_validity()

    def file_format_is_valid(self, file_path):
        return file_path.endswith('.txt')

    def process_directory(self, directory_path):
        print("processing directory...")
        valid_set = set(self.correct_files)
        for f in os.listdir(directory_path):
            full_path = os.path.join(directory_path, f)  # Chemin complet du fichier
            if os.path.isfile(full_path) and self.file_format_is_valid(full_path):
                if full_path not in valid_set:
                    if len(self.correct_files) >= self.max_file_amount:
                        self.step1_widget.show_warning(f"⚠️ Maximum file limit reached while processing {directory_path}.")
                        break
                    self.correct_files.append(full_path)  # Ajouter le chemin complet
                    self.step1_widget.add_file_to_correct_files_list_UI(full_path, True)
                    valid_set.add(full_path)
            else:
                if full_path not in self.invalid_files:
                    self.invalid_files.append(full_path)  # Ajouter le chemin complet pour les fichiers invalides aussi
                    self.step1_widget.add_file_to_correct_files_list_UI(full_path, False)


    def simplify_path(self, path):
        return os.path.basename(path)


class HelpWindow(SMiniWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Help")
        self.resize(400, 300)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.main_layout.addWidget(self.tree)

        self.add_help_step("Step 0: Welcome", "This is the welcoming message.\nYou can compare files and more.")
        self.add_help_step("Step 1: Select Comparison Type", "Choose whether you want to compare a single file with online data or multiple files.")
        self.add_help_step("Step 2: Choose Analysis Type", "Select whether you want a simple or complex analysis of your files.")

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


class GetInTouchWindow(SMiniWindow):
    def __init__(self):
        super().__init__()
        self.is_fully_init = False

        self.setWindowTitle("Get in touch")

        # Make the layout an instance attribute so it can be accessed later

        label = QLabel("Bug? Feature request? Commentary? Collab? We're all ears!")
        self.main_layout.addWidget(label)

    def full_init(self):
        self.add_contact_info(self.main_layout, "Daniel D.", ["Texts similarity computations", "UI (functional) and UX design", "Documentation"],
                              Mail="mailto:danieldefoing@gmail.com",
                              GitHub="https://github.com/Daniel-Dfg",
                              Discord="https://discord.com/users/720963652286414909")

        self.add_contact_info(self.main_layout, "LUCKYINS", ["Web scraping", "UI (styling)", "GitHub workflows"],
                              GitHub="https://github.com/Luckyyyin")

        self.add_contact_info(self.main_layout, "onuriscoding", ["UX Design", "GitHub workflows"],
                              GitHub="https://github.com/onuriscoding")

        self.add_contact_info(self.main_layout, "botEkrem", ["General Consultancy", "GitHub workflows", "Cross-platform compatibility (dockerization)"],
                              GitHub="https://github.com/BotEkrem")

        self.is_fully_init = True

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
            button = SButtons()
            button.setIcon(QIcon(f"Resources/Excess Files/UI_elements/{social}_icon.png"))
            button.setToolTip(social)
            button.clicked.connect(lambda _, link=kwargs[social]: webbrowser.open(link))
            contact_header_layout.addWidget(button)

        contact_header.setLayout(contact_header_layout)
        contact_layout.addWidget(contact_header)

        toggle_checkbox = QCheckBox("Show roles")
        toggle_checkbox.setStyleSheet("""
                    QCheckBox::indicator:checked {
                    background-color: rgba(255, 200, 200, 100);
                    }
                    QCheckBox::indicator {
                            border-radius: 5px;
                            background-color: rgba(255, 255, 255, 25);
                        }
                        """)
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


class GraphWindow(SMiniWindow):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.setWindowTitle("Graphs [find an explicit title]")
        self.is_dark_mode = False


        next_previous_buttons_layout = QHBoxLayout()
        self.previous_button = SButtons("Previous Graph")
        self.previous_button.clicked.connect(self.show_previous_graph)
        self.next_button = SButtons("Next Graph")
        self.next_button.clicked.connect(self.show_next_graph)

        #self.save_button = SButtons("Save Graph")
        #self.save_button.clicked.connect(self.save_graph)
        next_previous_buttons_layout.addWidget(self.previous_button)
        next_previous_buttons_layout.addWidget(self.next_button)

        #button_layout.addWidget(self.save_button)

        self.main_layout.addLayout(next_previous_buttons_layout)

        self.toggle_theme_button = SButtons("Dark Theme")
        self.toggle_theme_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.toggle_theme_button, alignment=Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignTop) #TODO : remove this to let it be toggled by global dark theme, when ABCODIN will be done with UI implementation

        self.chart_view = QChartView()
        self.main_layout.addWidget(self.chart_view)

        # Data structure to store graphs
        self.graph_data = {}
        self.graph_names = []
        self.current_graph_index = 0

    def add_FreqDist_graph(self, name, freq_dist1, freq_dist2, x_label, y_label, title):
        # Merge and filter data
        all_keys = set(freq_dist1.keys()).union(set(freq_dist2.keys()))
        total_frequencies = {key: freq_dist1.get(key, 0) + freq_dist2.get(key, 0) for key in all_keys}
        sorted_keys = sorted(total_frequencies.keys(), key=lambda k: total_frequencies[k], reverse=True)[:20]

        #TODO : think about an optimization (might loop too much times over the same data...)
        y_data1 = [freq_dist1.get(key, 0) for key in sorted_keys]
        y_data2 = [freq_dist2.get(key, 0) for key in sorted_keys]

        self.graph_data[name] = (sorted_keys, y_data1, y_data2, x_label, y_label, title)
        self.graph_names.append(name)
        self.show_graph(name)

    def add_LengthPlot_graph(self, name, lengths1, lengths2, x_label, y_label, title):
        max_length = max(len(lengths1), len(lengths2))
        lengths1 += [0] * (max_length - len(lengths1))
        lengths2 += [0] * (max_length - len(lengths2))
        x_data = [str(i) for i in range(1, max_length + 1)]

        self.graph_data[name] = (x_data, lengths1, lengths2, x_label, y_label, title)
        self.graph_names.append(name)
        self.show_graph(name)

    def show_graph(self, name):
        """
        Problem : pseudo OOR (will fix via preloading), clicking once doesn't do anything...
        """
        if name not in self.graph_data:
            raise AttributeError(f"No graph named '{name}' found.")

        x_data, y_data1, y_data2, x_label, y_label, title = self.graph_data[name]

        chart = QChart()
        chart.setTitle(title)

        series = QBarSeries()
        set1 = QBarSet("Text 1")
        set2 = QBarSet("Text 2")

        set1.append(y_data1)
        set2.append(y_data2)
        series.append(set1)
        series.append(set2)

        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(x_data)
        axis_x.setTitleText(x_label)
        axis_x.setLabelsAngle(-90)

        axis_y = QValueAxis()
        axis_y.setTitleText(y_label)
        axis_y.applyNiceNumbers()

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        self.apply_theme(chart)  # Appliquer le thème actuel

        self.chart_view.setChart(chart)

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

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.show_graph(self.graph_names[self.current_graph_index])  # Recharger le graphique pour appliquer le thème

    def apply_theme(self, chart):
        if self.is_dark_mode:
            chart.setBackgroundBrush(QColor(0, 0, 0, 50))
            chart.setTitleBrush(QColor("#dddddd"))
            for axis in chart.axes():
                axis.setLabelsBrush(QColor("#dddddd"))
                axis.setLinePenColor(QColor("#dddddd"))
                axis.setGridLineColor(QColor("#444444"))
        else:
            chart.setBackgroundBrush(QColor(255, 255, 255, 50))
            chart.setTitleBrush(QColor("#000000"))
            for axis in chart.axes():
                axis.setLabelsBrush(QColor("#000000"))
                axis.setLinePenColor(QColor("#000000"))
                axis.setGridLineColor(QColor("#cccccc"))

    #WILL PROBABLY BE GROUPED WITH OTHER SAVE METHODS IN A DEDICATED CLASS (like exporting full data in JSON or stuff like that)
    """
    def save_graph(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if file_path:
            pixmap = self.chart_view.grab()
            pixmap.save(file_path)
    """
