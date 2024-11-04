from matplotlib.backends.backend_agg import RendererAgg
from nltk.corpus.reader import toolbox
from nltk.probability import SimpleGoodTuringProbDist
from nltk.tokenize.api import overridden
from typing_extensions import override
from PySide6.QtWidgets import  QLabel, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QFrame, QCheckBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import  QColor, QIcon
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
import os
import webbrowser
from UI_Styling.sdroparea import SDropArea
from UI_Styling.smainwindow import SMainWindow
from UI_Styling.sminiwindow import SMiniWindow
from UI_Styling.sbuttons import SButtons
MAX_FILES_AMOUNT = 5 #TODO : find a solution to keep the same value in stacked_widget_elems (might be a bit early for a global constants file)


class DropArea(SDropArea):
    def __init__(self, step1_widget, max_file_amount=5):
        super().__init__()
        self.setAcceptDrops(True)
        # Error message
        self.errormessage = ""
        self.max_file_amount = max_file_amount
        self.step1_widget = step1_widget
        self.min_file_amount = 1 if max_file_amount == 1 else 2

        self.correct_files = []
        self.invalid_files = []

    @override
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    @override
    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        valid_set = set(self.correct_files)
        for file in files:
            if os.path.isfile(file) and self.file_format_is_valid(file) and file not in valid_set:
                if len(self.correct_files) < self.max_file_amount:
                    self.correct_files.append(file)
                    self.step1_widget.add_file_to_correct_files_list_UI(simplify_path(file), True)
                    valid_set.add(file)
                else:
                    self.errormessage = "⚠️ Maximum file limit reached!"
            elif os.path.isdir(file):
                self.process_directory(file)
            else:
                if file not in valid_set:
                    self.errormessage = f"⚠️ .{file.split('.')[-1]} is not a valid file format."
        self.step1_widget.update_current_content_validity()

    def file_format_is_valid(self, file_path):
        return file_path.endswith('.txt') #TODO : support other file types (.pdf, .md...)

    def process_directory(self, directory_path):
        valid_set = set(self.correct_files)
        for f in os.listdir(directory_path):
            full_path = os.path.join(directory_path, f)
            if os.path.isfile(full_path) and self.file_format_is_valid(full_path):
                if full_path not in valid_set:
                    if len(self.correct_files) >= self.max_file_amount:
                        self.errormessage = f"⚠️ Maximum file limit reached while processing {directory_path}."
                        break
                    self.correct_files.append(full_path)
                    self.step1_widget.add_file_to_correct_files_list_UI(simplify_path(full_path), True)
                    valid_set.add(full_path)
            else:
                if full_path not in self.invalid_files:
                    self.invalid_files.append(full_path)
                    self.step1_widget.add_file_to_correct_files_list_UI(simplify_path(full_path), False)

class HelpWindow(SMiniWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.resize(400, 300)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.main_layout.addWidget(self.tree)


        self.add_help_step("Step 0: Pick a type of analysis",
                            "Compare a single file with online data or files between each other (useful for students, for example : they can compare their texts that way)")
        self.add_help_step("Step 1: Choose your desired files",
                            "We support drag & dropping and browsing files/folders.\nValid content will be automatically extracted from a provided folder, with its invalid files being shown in the \"invalid files\" section.")
        self.add_help_step("Step 2: Choose Analysis Type",
                            "The difference between the simple and complex analysis stands in the fact that complex analysis extends the simple analysis, helping to provide more insights while being more computation-heavy.")
        self.add_help_step("Step 3: Results",
                            "All of these numbers and terms can be overwhelming for many, so let's explain these one by one very simply :\n"
                            "- Text richness = number_of_different_terms / total_number_of_terms\n"
                            "Cosine and Jaccard similarity are similarity computations based on several factors : the position of words in a text, the amount of times they appear in total, etc. They're known to be among the most accurate text similarity algorithms we know today.\n"
                            "You might've noticed than, if you decided to do a \"Complex Analysis\", Cosine and Jaccard similarity both appear twice : they're applied once on the 'words' of each pair of texts, and once on the 'pos' of each pair of text... But what does 'pos' mean ?\n"
                            "Well - POS is an abbreviation for \"Part(s) Of Speech\", which indicates the 'class' of a given word in a text (noun, pronoun, adjective, determinant...).\n"
                            "So we compute similarity between the POS of each pair of text because, if two texts are structurally similar (their sentences are \"built the same way\", if you wish), it's going to show up in these computations !")
        self.add_help_step("(Optional) Graph Window",
            "When looking at the results, if you click the 'show graphs' button, a button displaying some graphs will appear : they're here to help you visualize how the texts you provided are (dis)similar to each other.\n"
            "There is just one thing we must clarify in these :\n"
            "The meaning of 'bigrams' (and 'trigrams' in the case of a complex analysis) : n-grams are sequences of n contiguous words in a text. In the sentence \"I ate an apple\", the BIgrams are 'I ate', 'ate an', and 'an apple'.\n")

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
        self.setFixedSize(550, 580)
        self.is_fully_init = False
        self.checkBoxs = []
        self.rolesWidget = []

        self.setWindowTitle("Get in touch")

        #self.lay_out = QVBoxLayout()

        label = QLabel("Bug? Feature request? Commentary? Collab? We're all ears!")
        self.main_layout.addWidget(label)
        #QTimer.singleShot(180, self.full_init)

    def full_init(self):
        self.add_contact_info(self.main_layout, "Daniel-Dfg", ["Lead developer", "Texts similarity computations", "UI design (functional)", "Documentation gathering and handling"],
                              Mail="mailto:danieldefoing@gmail.com",
                              GitHub="https://github.com/Daniel-Dfg",
                              Discord="https://discord.com/users/720963652286414909")

        self.add_contact_info(self.main_layout, "LUCKYINS", ["Repo manager and Bugs fixer","Web scraping", "UI design (styling)", "Documentation gathering"],
                              Mail="mailto:elhusseinabdalrahmanwork@gmail.com",
                              GitHub="https://github.com/LUCKYINS",
                              Discord="https://discord.com/users/721008804300455978")

        self.add_contact_info(self.main_layout, "onuriscoding", ["UX Design", "GitHub workflows"],
                              Mail="mailto:onurdogancs@gmail.com",
                              GitHub="https://github.com/onuriscoding",
                              Discord="https://discord.com/users/332553376707510272")

        self.add_contact_info(self.main_layout, "botEkrem", ["General Consultancy", "GitHub workflows", "Dockerization"],
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
        self.checkBoxs.append(toggle_checkbox)
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
        self.rolesWidget.append(roles_widget)
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
            for i in range(len(self.checkBoxs)):
                if toggle_checkbox != self.checkBoxs[i]:
                    self.checkBoxs[i].setChecked(False)
                    self.checkBoxs[i].setText("Show roles")
                    self.rolesWidget[i].setVisible(False)
            toggle_checkbox.setText("Hide roles")
            roles_widget.setVisible(True)
            self.setFixedSize(550, 680)
        else:
            self.setFixedSize(550, 580)
            toggle_checkbox.setText("Show roles")
            roles_widget.setVisible(False)


class GraphWindow(SMiniWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphs")
        self.is_dark_mode = False

        next_previous_buttons_layout = QHBoxLayout()
        self.previous_button = SButtons("Previous")
        self.previous_button.clicked.connect(self.show_previous_graph)
        self.next_button = SButtons("Next")
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

        self.graph_data = {}
        self.graph_names = []
        self.current_graph_index = 0

    def add_FreqDist_graph(self, name, freq_dist1, freq_dist2, x_label, y_label, title):
        # Merge and filter data
        all_keys = set(freq_dist1.keys()).union(set(freq_dist2.keys()))
        total_frequencies = {key: freq_dist1.get(key, 0) + freq_dist2.get(key, 0) for key in all_keys}
        sorted_keys = sorted(total_frequencies.keys(), key=lambda k: total_frequencies[k], reverse=True)[:20]

        #TODO : think about an optimization (might loop too much times over the same data...)
        y_data1 = [float(freq_dist1.get(key, 0)) for key in sorted_keys]
        y_data2 = [float(freq_dist2.get(key, 0)) for key in sorted_keys]

        self.graph_data[name] = ([' '.join(key) if isinstance(key, tuple) else key for key in sorted_keys],
                                y_data1, y_data2, x_label, y_label, title)
        if name not in self.graph_names:
            self.graph_names.append(name)
            self.current_graph_index = len(self.graph_names) - 1
        self.show_graph(name)

    def add_LengthPlot_graph(self, name, lengths1, lengths2, x_label, y_label, title):
        max_length = max(len(lengths1), len(lengths2))
        lengths1 += [0] * (max_length - len(lengths1))
        lengths2 += [0] * (max_length - len(lengths2))
        x_data = [str(i) for i in range(1, max_length + 1)]

        self.graph_data[name] = (x_data, lengths1, lengths2, x_label, y_label, title)
        if name not in self.graph_names:
            self.graph_names.append(name)
            self.current_graph_index = len(self.graph_names) - 1
        self.show_graph(name)

    def show_graph(self, name):
        if name not in self.graph_data:
            raise AttributeError(f"No graph named '{name}' found.")

        x_data, y_data1, y_data2, x_label, y_label, title = self.graph_data[name]

        chart = QChart()
        chart.setTitle(title)
        series = QBarSeries()
        set1 = QBarSet("File 1")
        set1.setColor("#634747" if self.is_dark_mode else "#eba5a5")
        set2 = QBarSet("File 2")
        set2.setColor("#a6d7e7" if self.is_dark_mode else "#475c63")

        set1.append(y_data1)
        set2.append(y_data2)
        series.append(set1)
        series.append(set2)

        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(x_data)
        axis_x.setTitleText(x_label)
        axis_x.setLabelsColor("#e6e6e6" if self.is_dark_mode else "#232023")
        axis_x.setLabelsAngle(-90)
        axis_y = QValueAxis()
        axis_y.setTitleText(y_label)
        axis_y.setLabelsColor("#e6e6e6" if self.is_dark_mode else "#232023")
        axis_y.applyNiceNumbers()

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        self.apply_theme(chart)
        self.chart_view.setChart(chart)

    def show_previous_graph(self):
        if self.graph_names:
            self.current_graph_index = (self.current_graph_index - 1) % len(self.graph_names)
            self.show_graph(self.graph_names[self.current_graph_index])
    def show_next_graph(self):
        if self.graph_names:
            self.current_graph_index = (self.current_graph_index + 1) % len(self.graph_names)
            self.show_graph(self.graph_names[self.current_graph_index])
    def toggle_theme(self):
            self.is_dark_mode = not self.is_dark_mode
            self.show_graph(self.graph_names[self.current_graph_index])  # Recharger le graphique pour appliquer le thème

    def apply_theme(self, chart):
        if self.is_dark_mode:
            chart.setBackgroundBrush(QColor("#232023"))
            chart.setTitleBrush(QColor("#e6e6e6"))

            for axis in chart.axes():
                axis.setLabelsBrush(QColor("#e6e6e6"))
                axis.setLinePenColor(QColor("#dddddd"))
                axis.setGridLineColor(QColor("#444444"))
        else:
            chart.setBackgroundBrush(QColor("#ffffff"))
            chart.setTitleBrush(QColor("#232023"))
            for axis in chart.axes():
                axis.setLabelsBrush(QColor("#232023"))
                axis.setLinePenColor(QColor("#232023"))
                axis.setGridLineColor(QColor("#cccccc"))

    #WILL PROBABLY BE GROUPED WITH OTHER SAVE METHODS IN A DEDICATED CLASS (like exporting full data in JSON or stuff like that)
    """
    def save_graph(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if file_path:
            pixmap = self.chart_view.grab()
            pixmap.save(file_path)
    """


def simplify_path(file_path):
    parent_dir = os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    return os.path.join(parent_dir, file_name)
