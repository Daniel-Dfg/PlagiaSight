from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
                             QListWidget, QHBoxLayout, QComboBox, QRadioButton,
                             QButtonGroup, QProgressBar, QHBoxLayout)
from PySide6.QtCore import Qt, QTimer, Signal
from .comparison_results import OneFileComparison, CrossCompare
from nltk import FreqDist
from .utilities import DropArea, GraphWindow

#GLOBAL CONSTANTS : characteristics with their attributes equivalents (to get them via the getattr() built-in Python method later on)
#Characteristics independent to each text (found in the TokenStatsAndRearrangements instance each text is in)
INDIV_CHARACTERISTICS = ["Text Richness", "average sentence length", "median sentence length"]
INDIV_CHARS_ATTRS = ["text_richness", "average_sent_length", "median_sent_length"]

### SIMPLE ANALYSIS ###
#Characteristics common to each 'duo' of texts (found in the TextComparisonAlgorithms instance they're both in)
COMMON_CHARS_SIMPLE = ["Cosine sim (words)", "Jaccard sim (words)"]
COMMON_CHARS_SIMPLE_ATTRS =  ["cosine_sim_words", "jaccard_sim_words"]
#Characteristics common to each 'duo' of texts to be displayed in graphics
GRAPH_COMMON_CHARS_SIMPLE = ["word frequency (top 20%)", "Sentences length (plotting)"]
GRAPH_COMMON_CHARS_SIMPLE_ATTRS = ["word_freq", "sent_lengths"] #the 'top 20%' of most frequent terms will be filtered from the word_freq attribute, that initially is a FreqDist of ALL terms
#######################

### COMPLEX ANALYSIS ###
#Same idea as Simple analysis' global constants. Notice how the complex analysis is essentially an "extension" of the simple analysis !
COMMON_CHARS_COMPLEX = COMMON_CHARS_SIMPLE + ["Cosine sim (pos)", "Jaccard sim (pos)"]
COMMON_CHARS_COMPLEX_ATTRS = COMMON_CHARS_SIMPLE_ATTRS + ["cosine_sim_pos", "jaccard_sim_pos"]
GRAPH_COMMON_CHARS_COMPLEX = GRAPH_COMMON_CHARS_SIMPLE + ["most common bigrams (top 20%)", "most common trigrams (top 20%)"]
GRAPH_COMMON_CHARS_COMPLEX_ATTRS = GRAPH_COMMON_CHARS_SIMPLE_ATTRS + ["bigrams", "trigrams"] #same remark as for word_freq (see GRAPH_COMMON_CHARS_SIMPLE_ATTRS)
#########################

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
        self.textual_display_common_func_labels = COMMON_CHARS_SIMPLE_ATTRS if self.main_window.step3_widget.analysis_complexity == "simple" else COMMON_CHARS_COMPLEX_ATTRS

        self.graphical_display_elems_names = GRAPH_COMMON_CHARS_SIMPLE if self.main_window.step3_widget.analysis_complexity == "simple" else GRAPH_COMMON_CHARS_COMPLEX
        self.graphical_display_func_labels = GRAPH_COMMON_CHARS_SIMPLE_ATTRS if self.main_window.step3_widget.analysis_complexity == "simple" else GRAPH_COMMON_CHARS_COMPLEX_ATTRS

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
        for char_name, char_label in zip(INDIV_CHARACTERISTICS, INDIV_CHARS_ATTRS):
            res_file1 = getattr(results.content_stats[file1], char_label)
            res_file2 = getattr(results.content_stats[file2], char_label)
            # Mettre à jour les labels directement
            self.file1_result_labels[char_name].setText(str(res_file1))
            self.file2_result_labels[char_name].setText(str(res_file2))

        if isinstance(self.main_window.final_results, OneFileComparison):
            # TODO : specific treatment for OneFileComp ?
            for common_char_name, common_char_label in zip(self.textual_display_common_charcs, self.textual_display_common_func_labels):
                common_res = getattr(results.get_comparison(file2), common_char_label)
                self.common_result_labels[common_char_name].setText(str(common_res))
        else:
            for common_char_name, common_char_label in zip(self.textual_display_common_charcs, self.textual_display_common_func_labels):
                common_res = getattr(results.get_comparison(file1, file2), common_char_label)
                self.common_result_labels[common_char_name].setText(str(common_res))

    def prepare_graphs_data(self):
        file1, file2 = self.left_content_title.currentText(), self.right_content_title.currentText()
        results = self.main_window.final_results
        graphs_data = []

        for char_name, char_label in zip(self.graphical_display_elems_names, self.graphical_display_func_labels):
            res_file1 = getattr(results.content_stats[file1], char_label)
            res_file2 = getattr(results.content_stats[file2], char_label)

            graphs_data.append((char_name, res_file1, res_file2))

        return graphs_data

    def view_graph(self):
        graphs_data = self.prepare_graphs_data()
        self.graph_window = GraphWindow(self.main_window)

        for graph_name, res_file1, res_file2 in graphs_data:
            freq_dist1 = res_file1
            freq_dist2 = res_file2
            self.graph_window.add_graph(
                name=graph_name,
                freq_dist1=freq_dist1,
                freq_dist2=freq_dist2,
                x_label="Items",
                y_label="Frequency",
                title=f"{graph_name} Comparison"
            )

        self.graph_window.show()
        #TODO : fix the logic of this
        self.left_content_title.currentIndexChanged.connect(self.update_graph_window)
        self.right_content_title.currentIndexChanged.connect(self.update_graph_window)

    def update_graph_window(self):
        if self.graph_window:  # Vérifiez si la fenêtre du graphique est déjà ouverte
            new_graphs_data = self.prepare_graphs_data()
            for graph_name, res_file1, res_file2 in new_graphs_data:
                freq_dist1 = FreqDist(dict(res_file1))
                freq_dist2 = FreqDist(dict(res_file2))
                self.graph_window.update_graph(
                    name=graph_name,
                    freq_dist1=freq_dist1,
                    freq_dist2=freq_dist2,
                    x_label="Items",
                    y_label="Frequency",
                    title=f"{graph_name} Comparison"
                )
