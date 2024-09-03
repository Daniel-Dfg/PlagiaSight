
from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSpacerItem, QSizePolicy, QTreeWidgetItem, QTreeWidget, QStackedWidget, QTextEdit, QFileDialog, QComboBox, QListWidget, QRadioButton, QButtonGroup, QProgressBar
from PySide6.QtCore import Qt, QUrl, Signal, QTimer
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent, QStandardItem, QStandardItemModel
import webbrowser
import os
from TextAnalysis_AkaPhase1 import *
from phase2 import *
from random import randint
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import arange
from sys import argv
#TODO : fix logic for step 1 directory drop (an invalid directory should not overwrite a previous valid one)
#TODO : rethink the overall logic of the stacked widgets to make it easier to manipulate,
#notably by adding more attrs to the MainWindow to keep the logic consistent


#TODO : rename global constants to be shorter
INDIV_CHARACTERISTICS = ["Text Richness", "average sentence length", "median sentence length"]
INDIV_CHARS_FUNCTS = ["text_richness", "average_sent_length", "median_sent_length"]

COMMON_CHARS_SIMPLE = ["Cosine sim (words)", "Jaccard sim (words)"]
COMMON_CHARS_SIMPLE_FUNCTS =  ["cosine_sim_words", "jaccard_sim_words"]
GRAPH_COMMON_CHARS_SIMPLE = ["word frequency (top 20% or so)", "Sentences length (plotting)"]
GRAPH_COMMON_CHARS_SIMPLE_FUNCTS = ["word_freq", "sent_lengths"]

COMMON_CHARS_COMPLEX = COMMON_CHARS_SIMPLE + ["Cosine sim (pos)", "Jaccard sim (pos)"]
COMMON_CHARS_COMPLEX_FUNCTS = COMMON_CHARS_SIMPLE_FUNCTS + ["cosine_sim_pos", "jaccard_sim_pos"]
GRAPH_COMMON_CHARS_COMPLEX = GRAPH_COMMON_CHARS_SIMPLE + ["most common bigrams (top 20% or so)", "most common trigrams (top 20% or so)"]
GRAPH_COMMON_CHARS_COMPLEX_FUNCTS = GRAPH_COMMON_CHARS_SIMPLE_FUNCTS + ["bigrams", "trigrams"] #TODO : reevaluate this expr

<<<<<<< Updated upstream
TEXTUAL_DISPLAY_COMMON_CHARACS_COMPLEX_ANALYSIS = TEXTUAL_DISPLAY_COMMON_CHARACS_SIMPLE_ANALYSIS + ["Cosine sim (pos)", "Jaccard sim (pos)"]
TEX_DIS_COMPLEX_COMMON_FUNC_EQUIVALENTS = TEX_DIS_SIMPLE_COMMON_FUNC_EQUIVALENTS + ["cosine_sim_pos", "jaccard_sim_pos"]
GRAPH_DISPLAY_COMMON_CHARACS_COMPLEX_ANALYSIS = GRAPH_DISPLAY_COMMON_CHARACS_SIMPLE_ANALYSIS + ["most common bigrams (top 20% or so)", "most common trigrams (top 20% or so)"]
GRAPH_DISPLAY_COMMON_FUNC_EQUIVALENTS_COMPLEX = GRAPH_DISPLAY_COMMON_FUNC_EQUIVALENTS_SIMPLE + ["most_common_bigrams", "most_common_trigrams"] #TODO : reevaluate this expr
=======
>>>>>>> Stashed changes

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

class Step0_WelcomingMessage(QWidget):
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
        self.main_window.expected_type = expected_type
        self.main_window.step1_widget = Step1_FileDropAndCheck(self.main_window)
        self.main_window.stacked_widget.addWidget(self.main_window.step1_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step1_widget)
        self.main_window.help_window.expand_step(1)

class Step1_FileDropAndCheck(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        self.label = QLabel("Drop your files or directories below or click 'Browse':")
        layout.addWidget(self.label)

        warning_layout = QVBoxLayout()
        self.warning_label = QLabel("")
        warning_layout.addWidget(self.warning_label)

        self.drop_area = DropArea(self.main_window.expected_type, self)
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
        if self.main_window.expected_type == "file":
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
        elif self.main_window.expected_type == "directory":
            directory_path = QFileDialog.getExistingDirectory(self, "Select a directory with .txt files")
            if directory_path:
                self.drop_area.process_directory(directory_path)

    def proceed_to_step2(self):
        print("Proceeding to step 2 with files:", self.drop_area.correct_files)
        if not hasattr(self.main_window, "step2_widget"):
            self.main_window.step2_widget = Step2_AnalysisComplexityPick(self.main_window)
        self.main_window.stacked_widget.addWidget(self.main_window.step2_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step2_widget)
        self.main_window.help_window.expand_step(2)

class Step2_AnalysisComplexityPick(QWidget):
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

        self.go_back_button = QPushButton("Back")
        self.go_back_button.clicked.connect(self.go_back)
        layout.addWidget(self.go_back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.simple_analysis_radio.toggled.connect(self.update_description)
        self.complex_analysis_radio.toggled.connect(self.update_description)

        self.setLayout(layout)

    def go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(1)
        self.main_window.help_window.expand_step(1)

    def update_description(self):
        if self.simple_analysis_radio.isChecked():
            self.description_label.setText("Simple Analysis: A quick overview of the files.")
            self.launch_button.setEnabled(True)
        elif self.complex_analysis_radio.isChecked():
            self.description_label.setText("Complex Analysis: A detailed and thorough analysis.")
            self.launch_button.setEnabled(True)

    def launch_analysis(self):
        selected_analysis = "simple" if self.simple_analysis_radio.isChecked() else "complex"
        print(f"Launching {selected_analysis} Analysis")

        #Move on to Step3Widget
        self.main_window.step3_widget = Step3_LoadResults(self.main_window, selected_analysis)
        self.main_window.stacked_widget.addWidget(self.main_window.step3_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step3_widget)
        self.main_window.help_window.expand_step(3)

class Step3_LoadResults(QWidget):
    done = Signal()
    def __init__(self, main_window, analysis_complexity):

        super().__init__()
        self.main_window = main_window
        self.next_button = QPushButton("Next")
        self.analysis_complexity = analysis_complexity

        layout = QVBoxLayout()

        self.current_file_processed_label = QLabel("Processing: None")
        layout.addWidget(self.current_file_processed_label)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)

        self.done.connect(lambda: QTimer.singleShot(300, self.move_to_step4))

        self.setLayout(layout)

        self.comparison_content = None
        self.process_files()

    def process_files(self):
        content = self.main_window.step1_widget.drop_area.correct_files
        #type = self.main_window.expected_type #file or directory
        if len(content) == 1:
            #web scraping, etc
            ...
            print("processing indiv")
            self.main_window.final_results = OneFileComparison(content[0], self.analysis_complexity)
        else:
            ...
            print("processing a set of FILES")
            #compare files between each other
            self.main_window.final_results = CrossCompare(files_paths=content, comparison_type=self.analysis_complexity)


        # Mark all as complete
        self.current_file_processed_label.setText("Processing: Complete")
        #TODO : update the progress bar value properly (probably by making it a mainWindow attr)
        self.progress_bar.setValue(100)
        self.done.emit()


    def move_to_step4(self):
        if not hasattr(self.main_window, 'step4_widget'):
            self.main_window.step4_widget = Step4_DisplayResults(self.main_window)
        self.main_window.stacked_widget.addWidget(self.main_window.step4_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step4_widget)
        self.main_window.help_window.expand_step(4)

class Step4_DisplayResults(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        graph_view_button = QPushButton("View Graph")
        graph_view_button.clicked.connect(self.view_graph)
        layout.addWidget(graph_view_button, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Comparison Results")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        file_selection_layout = QHBoxLayout()
        self.right_content_title = QComboBox()

        if isinstance(self.main_window.final_results, OneFileComparison):
            self.left_content_title = QComboBox()
            self.left_content_title.addItem(self.main_window.final_results.source_file)
            right_items = sorted(list(self.main_window.final_results.comparison_with.keys())) #the site names
            self.right_content_title.addItems(right_items)
        elif isinstance(self.main_window.final_results, CrossCompare):
            self.left_content_title = QComboBox()
            self.left_content_title.addItems(self.main_window.step1_widget.drop_area.correct_files)
            right_items = self.main_window.step1_widget.drop_area.correct_files
            self.right_content_title.addItems(right_items)
            self.right_content_title.removeItem(0)
            self.left_content_title.currentIndexChanged.connect(self.update_results)
        else:
            raise TypeError("Unexpected type for final_results")

        file_selection_layout.addWidget(QLabel("File 1:"))
        file_selection_layout.addWidget(self.left_content_title)
        file_selection_layout.addWidget(QLabel("File 2:"))
        file_selection_layout.addWidget(self.right_content_title)

        layout.addLayout(file_selection_layout)

        # Dictionnaires pour stocker les labels des résultats
        self.file1_result_labels = {}
        self.file2_result_labels = {}
        self.common_result_labels = {}

        # Créer les lignes pour chaque caractéristique
        self.textual_display_common_charcs = COMMON_CHARS_SIMPLE if self.main_window.step3_widget.analysis_complexity == "simple" else COMMON_CHARS_COMPLEX
        self.textual_display_common_func_labels = COMMON_CHARS_SIMPLE_FUNCTS if self.main_window.step3_widget.analysis_complexity == "simple" else COMMON_CHARS_COMPLEX_FUNCTS

<<<<<<< Updated upstream
        self.graphical_display_elems_names = GRAPH_DISPLAY_COMMON_CHARACS_SIMPLE_ANALYSIS if self.main_window.step3_widget.analysis_type == "simple" else GRAPH_DISPLAY_COMMON_CHARACS_COMPLEX_ANALYSIS
        self.graphical_display_func_labels = GRAPH_DISPLAY_COMMON_FUNC_EQUIVALENTS_SIMPLE if self.main_window.step3_widget.analysis_type == "simple" else GRAPH_DISPLAY_COMMON_FUNC_EQUIVALENTS_COMPLEX
=======
        self.graphical_display_elems_names = GRAPH_COMMON_CHARS_SIMPLE if self.main_window.step3_widget.analysis_complexity == "simple" else GRAPH_COMMON_CHARS_COMPLEX
        self.graphical_display_func_labels = GRAPH_COMMON_CHARS_SIMPLE_FUNCTS if self.main_window.step3_widget.analysis_complexity == "simple" else GRAPH_COMMON_CHARS_COMPLEX_FUNCTS

>>>>>>> Stashed changes
        for char in INDIV_CHARACTERISTICS:
            line_layout = QHBoxLayout()

            char_label = QLabel(char)
            common_result_label = QLabel("-")
            result2_label = QLabel("-")

            line_layout.addWidget(char_label)
            line_layout.addWidget(common_result_label)
            line_layout.addWidget(result2_label)

            # Stocker les labels dans les dictionnaires
            self.file1_result_labels[char] = common_result_label
            self.file2_result_labels[char] = result2_label

            layout.addLayout(line_layout)

        # Ajouter les caractéristiques communes
        for common_char in self.textual_display_common_charcs:
            line_layout = QHBoxLayout()

            char_label = QLabel(common_char)
            common_result_label = QLabel("C")

            line_layout.addWidget(char_label)
            line_layout.addWidget(common_result_label)
            self.common_result_labels[common_char] = common_result_label

            layout.addLayout(line_layout)

        self.setLayout(layout)
        self.right_content_title.currentIndexChanged.connect(self.update_results)
        self.update_results()

    def update_results(self):
        print("updating textual results")
        file1, file2 = self.left_content_title.currentText(), self.right_content_title.currentText()
        results = self.main_window.final_results
        for char_name, char_label in zip(INDIV_CHARACTERISTICS, INDIV_CHARS_FUNCTS):
            res_file1 = getattr(results.file_stats[file1], char_label)
            res_file2 = getattr(results.file_stats[file2], char_label)
            # Mettre à jour les labels directement
            self.file1_result_labels[char_name].setText(str(res_file1))
            self.file2_result_labels[char_name].setText(str(res_file2))

        if isinstance(self.main_window.final_results, OneFileComparison):
            ...
            print("Not done yet")
            raise

        else:
            for common_char_name, common_char_label in zip(self.textual_display_common_charcs, self.textual_display_common_func_labels):
                common_res = getattr(results.get_comparison(file1, file2), common_char_label)
                self.common_result_labels[common_char_name].setText(str(common_res))

    def prepare_graphs_data(self):
        file1, file2 = self.left_content_title.currentText(), self.right_content_title.currentText()
        results = self.main_window.final_results
        graphs_data = []

        for char_name, char_label in zip(self.graphical_display_elems_names, self.graphical_display_func_labels):
            res_file1 = getattr(results.file_stats[file1], char_label)
            res_file2 = getattr(results.file_stats[file2], char_label)
            if char_label == "term_freq": #side note : might not be the most clear to the reader to have this
                res_file1 = res_file1.most_common(int(len(res_file1) * 0.2))
                res_file2 = res_file2.most_common(int(len(res_file2) * 0.2))
                #needed later : iterate over the union of the elems to make a sorted dict[tuple[float, float]] ?

            categories = [f"{file1} {char_name}", f"{file2} {char_name}"]
            values = [res_file1, res_file2]
            graphs_data.append((categories, values))
        return graphs_data

    def view_graph(self):
        # Préparez les données initiales pour les graphiques
        graphs_data = self.prepare_graphs_data()

        # Instanciez et affichez la fenêtre de graphiques
        self.graph_window = GraphWindow(self.main_window)
        self.graph_window.show()

        # Connecter les ComboBoxes pour mettre à jour les graphiques dynamiquement
        self.left_content_title.currentIndexChanged.connect(self.update_graph_window)
        self.right_content_title.currentIndexChanged.connect(self.update_graph_window)

    def update_graph_window(self):
        if self.graph_window:  # Vérifiez si la fenêtre du graphique est déjà ouverte
            new_graphs_data = self.prepare_graphs_data()
            self.graph_window.update_graphs_data(new_graphs_data)


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphs: Sentence Length & Word Frequencies")
        layout = QVBoxLayout(self)

        # Configuration des boutons de navigation
        button_layout = QHBoxLayout()
        self.sentence_length_button = QPushButton("Sentence Length Graph")
        self.sentence_length_button.clicked.connect(self.show_sentence_length_graph)
        self.word_freq_button = QPushButton("Word Frequency Graph")
        self.word_freq_button.clicked.connect(self.show_word_freq_graph)
        button_layout.addWidget(self.sentence_length_button)
        button_layout.addWidget(self.word_freq_button)

        layout.addLayout(button_layout)

        # Ajout du canvas de Matplotlib
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

        # Initialisation de l'axe pour les graphiques
        self._static_ax = self.canvas.figure.subplots()

        # Génération des données aléatoires pour les graphiques
        self.sentence_length_data = self.generate_sentence_length_data()
        self.word_freq_data = self.generate_word_freq_data()

        # Affichage initial
        self.show_sentence_length_graph()

    def generate_sentence_length_data(self):
        """Génère des données fictives pour la longueur des phrases."""
        sentence_indices = np.arange(1, 11)  # Indices de phrases de 1 à 10
        lengths_text1 = np.random.randint(5, 20, size=10)  # Longueur des phrases du texte 1
        lengths_text2 = np.random.randint(5, 20, size=10)  # Longueur des phrases du texte 2
        return sentence_indices, lengths_text1, lengths_text2

    def generate_word_freq_data(self):
        """Génère des données fictives pour les fréquences de mots."""
        words = ['word1', 'word2', 'word3', 'word4', 'word5', 'word6']  # Liste des mots
        freq_text1 = np.random.randint(1, 15, size=len(words))  # Fréquence des mots pour le texte 1
        freq_text2 = np.random.randint(1, 15, size=len(words))  # Fréquence des mots pour le texte 2
        return words, freq_text1, freq_text2

    def show_sentence_length_graph(self):
        """Affiche le graphique comparant les longueurs de phrases."""
        self._static_ax.clear()
        indices, lengths_text1, lengths_text2 = self.sentence_length_data
        bar_width = 0.35
        index = np.arange(len(indices))
        self._static_ax.bar(index, lengths_text1, bar_width, label='Text 1')
        self._static_ax.bar(index + bar_width, lengths_text2, bar_width, label='Text 2')

        self._static_ax.set_xlabel('Sentence Index')
        self._static_ax.set_ylabel('Sentence Length')
        self._static_ax.set_title('Sentence Length Comparison')
        self._static_ax.set_xticks(index + bar_width / 2)
        self._static_ax.set_xticklabels(indices)
        self._static_ax.legend()
        self.canvas.draw()

    def show_word_freq_graph(self):
        """Affiche le graphique comparant les fréquences de mots."""
        self._static_ax.clear()
        words, freq_text1, freq_text2 = self.word_freq_data
        bar_width = 0.35
        index = np.arange(len(words))
        self._static_ax.bar(index, freq_text1, bar_width, label='Text 1')
        self._static_ax.bar(index + bar_width, freq_text2, bar_width, label='Text 2')

        self._static_ax.set_xlabel('Words')
        self._static_ax.set_ylabel('Frequency')
        self._static_ax.set_title('Word Frequency Comparison')
        self._static_ax.set_xticks(index + bar_width / 2)
        self._static_ax.set_xticklabels(words, rotation=45, ha="right")
        self._static_ax.legend()
        self.canvas.draw()



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



"""
Toutes les sources doivent passer par la tokenization et le TSAR pour les stats individuelles.
Par contre, seules les sources doivent passer par une lecture, et les textes en ligne doivent
passer par le web scraping.

Pour la cross-comparaison, on a des cas différents selon le type d'analyse :
    - Si on a 1 fichier, on doit comparer ce fichier avec les sources internet.
    - Si on a plusieurs fichiers, on doit comparer chaque fichier avec les autres fichiers.
"""

@dataclass
class OneFileComparison:
    """
    - Used when 1 file is provided (step 0)
    - In charge of web scraping and analysis with the resulting texts.
    """
    source_file : str # file path
    comparison_type : str # either "simple" or "complex"
    content_stats : dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False, default_factory=dict) #dict[site_name, TSAR]
    comparison_with : dict[str, TextProcessingAlgorithms] = field(init=False, repr=False, default_factory=dict) #dict[site_name, TPA]

    def __post_init__(self):
        #TODO : make this more explicit
        self.content_stats[self.source_file] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file(self.source_file)))
        source_file_keywords = {k: v for k, v in sorted(self.content_stats[self.source_file].keywords_scores.items(), key=lambda item: item[1], reverse=True)[:3]}
        for keyword in source_file_keywords.keys():
            u = URLs(keyword, 2)
            associated_urls = u.url_array
            for response in associated_urls:
                site_name = urlparse(response.url).netloc
                text = HtmlText(response)
                text.makeTempText()
                self.content_stats[site_name] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file("temp.txt")))
                self.comparison_with[site_name] = TextProcessingAlgorithms(self.content_stats[self.source_file], self.content_stats[site_name])

                #

        #links = get_links_from_keywords(self.source_data.base.find_keywords()) (pseudocode)
        #for link in links:
            #self.online_data[link] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_link(text)))
            #self.comparison_with[link] = TextProcessingAlgorithms(self.source_data, self.online_data[link])
        ...


@dataclass
class CrossCompare:
    """
    Used when a directory is provided (step 0).
    Compares the given files between eachother.
    """
    files_paths: list[str]
    comparison_type: str  # either "simple" or "complex"
    file_stats: dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False)  # Statistiques individuelles par fichier
    comparisons: dict[tuple[str, str], TextProcessingAlgorithms] = field(init=False, repr=False)  # Comparaisons entre les fichiers

    def __post_init__(self):
        self.file_stats = {}
        self.comparisons = {}
        if self.comparison_type not in ["simple", "complex"]:
            raise ValueError(f"Invalid comparison type. Must be either 'simple' or 'complex'. It is currently {self.comparison_type}.")

        # Générer les statistiques pour chaque fichier
        for file in self.files_paths:
            self.file_stats[file] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file(file)))

        # Comparer chaque fichier avec les autres
        for i, file1 in enumerate(self.files_paths):
            for j, file2 in enumerate(self.files_paths):
                if i < j:
                    print(f"Comparing {file1} with {file2}")
                    tsar1 = self.file_stats[file1]
                    tsar2 = self.file_stats[file2]
                    self.comparisons[(file1, file2)] = TextProcessingAlgorithms(tsar1, tsar2)
                    if self.comparison_type == "simple":
                        self.simple_analysis_two_files(file1, file2)
                        #self.comparisons[(file1, file2)].display_simple_results()
                    elif self.comparison_type == "complex":
                        self.complex_analysis_two_files(file1, file2)
                        #self.comparisons[(file1, file2)].display_complex_results()


    def simple_analysis_two_files(self, file1, file2) -> None:
        # just triggering the necessary computations that weren't done
        a, b = self.comparisons[(file1, file2)].cosine_sim_words, \
               self.comparisons[(file1, file2)].jaccard_sim_words

    def complex_analysis_two_files(self, file1, file2) -> None:
        self.simple_analysis_two_files(file1, file2)
        # additional computations
        a, b = self.comparisons[(file1, file2)].cosine_sim_pos, \
               self.comparisons[(file1, file2)].jaccard_sim_pos
        ...

    def get_comparison(self, file1: str, file2: str) -> TextProcessingAlgorithms:
        if (file1, file2) in self.comparisons:
            return self.comparisons[(file1, file2)]
        elif (file2, file1) in self.comparisons:
            return self.comparisons[(file2, file1)]
        else:
            raise ValueError("The comparison between these files does not exist.")



if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running from an IDE).
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(argv)

    window = MainWindow()
    window.show()
    window.raise_()
    qapp.exec()
