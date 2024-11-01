from typing_extensions import override
from PySide6.QtWidgets import (QGridLayout, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
                             QListWidget, QHBoxLayout, QComboBox, QRadioButton,
                             QButtonGroup, QProgressBar, QHBoxLayout, QListWidgetItem)
from PySide6.QtCore import Qt, QTimer, Signal, QEvent
from nltk.metrics.aline import align
from text_analysis import UnprocessableTextContent
from .comparison_results import OneFileComparison, CrossCompare
from nltk import FreqDist
from .utilities import DropArea, GraphWindow
from UI_Styling import slabels, sbuttons, filescontainer, sradiobuttons
from time import time

#GLOBAL CONSTANTS : characteristics with their attributes equivalents (to get them via the getattr() built-in Python method later on)
#Characteristics independent to each text (found in the TokenStatsAndRearrangements instance each text is in)
INDIV_CHARACTERISTICS = ["Text Richness", "average sentence length", "median sentence length"]
INDIV_CHARS_ATTRS = ["text_richness", "average_sent_length", "median_sent_length"]
CURRENT_TIME = None


### SIMPLE ANALYSIS ###
#Characteristics common to each 'duo' of texts (found in the TextComparisonAlgorithms instance they're both in)
COMMON_CHARS_SIMPLE = ["Cosine sim (words)", "Jaccard sim (words)"]
COMMON_CHARS_SIMPLE_ATTRS =  ["cosine_sim_words", "jaccard_sim_words"]
#Characteristics common to each 'duo' of texts to be displayed in graphics
GRAPH_COMMON_CHARS_SIMPLE = ["word frequency (top ???%)", "Sentences length (plotting)"]
GRAPH_COMMON_CHARS_SIMPLE_ATTRS = ["word_freq", "sent_lengths"] #the 'top 20%' of most frequent terms will be filtered from the word_freq attribute, that initially is a FreqDist of ALL terms
#######################

### COMPLEX ANALYSIS ###
#Same idea as Simple analysis' global constants. Notice how the complex analysis is essentially an "extension" of the simple analysis !
COMMON_CHARS_COMPLEX = COMMON_CHARS_SIMPLE + ["Cosine sim (pos)", "Jaccard sim (pos)"]
COMMON_CHARS_COMPLEX_ATTRS = COMMON_CHARS_SIMPLE_ATTRS + ["cosine_sim_pos", "jaccard_sim_pos"]
GRAPH_COMMON_CHARS_COMPLEX = GRAPH_COMMON_CHARS_SIMPLE + ["most common bigrams (top ???%)", "most common trigrams (top 20%)"]
GRAPH_COMMON_CHARS_COMPLEX_ATTRS = GRAPH_COMMON_CHARS_SIMPLE_ATTRS + ["bigrams", "trigrams"] #same remark as for word_freq (see GRAPH_COMMON_CHARS_SIMPLE_ATTRS)
#########################

MAX_FILES_AMOUNT = 5 #maximum amount of files comparable to each other at once

class Step0_WelcomingMessage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        #Labels
        sl1 = QLabel("PlagiaSight", self)
        sl2 = QLabel("A transparent plagiarism detection tool.", self)
        sl3 = QLabel("Compare...", self)

        #Labels fonts
        labels = {sl1:"64", sl2:"24", sl3:"32"}

        for label,font_size in labels.items():
            label.setStyleSheet(f"font-size: {font_size}px;")
            layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        button1 = sbuttons.SButtons("One file with related online data")
        button2 = sbuttons.SButtons("A set of files between each other")

        buttons = {button1: (lambda: self.proceed_to_next_step(1)), button2: (lambda: self.proceed_to_next_step(MAX_FILES_AMOUNT))}
        for button, func in buttons.items():
            button.clicked.connect(func)
            button.setFixedSize(280, 50)
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)


        self.setLayout(layout)

    def proceed_to_next_step(self, max_files_amount):
        self.main_window.max_files_amount = max_files_amount
        self.main_window.step1_widget = Step1_FileDropAndCheck(self.main_window)
        self.main_window.stacked_widget.addWidget(self.main_window.step1_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step1_widget)
        self.main_window.help_window.expand_step(1)


class Step1_FileDropAndCheck(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QGridLayout(self)

        self.drop_area = DropArea(self, self.main_window.max_files_amount)
        layout.addWidget(self.drop_area,0,0, alignment=Qt.AlignmentFlag.AlignCenter |Qt.AlignmentFlag.AlignLeft)

        self.drop_area.browseFiles.clicked.connect(self._browse_single_file)
        if self.main_window.max_files_amount == MAX_FILES_AMOUNT:
            self.drop_area.browseFolders.setDisabled(False)
            self.drop_area.browseFolders.setHidden(False)
            self.drop_area.browseFolders.clicked.connect(self._browse_directory)

        self.filesContainers = filescontainer.FilesContainer()
        self.correct_files_label = self.filesContainers.validContainer.label
        self.correct_files_label.setText(f"Valid files (0 / {self.main_window.max_files_amount})")
        self.invalid_files_label = self.filesContainers.validContainer.label
        self.correct_files_list = self.filesContainers.validContainer.container
        self.invalid_files_list = self.filesContainers.invalidContainer.container
        layout.addWidget(self.filesContainers, 0,1)

        bottom_layout = QHBoxLayout()
        self.back_button = sbuttons.SButtons("Back")
        self.back_button.clicked.connect(self.go_back)
        bottom_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.status_label = QLabel("Nothing dropped yet!")
        self.status_label.setStyleSheet("font-size:20px;color:white;")
        bottom_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.next_button = sbuttons.SButtons("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.proceed_to_next_step)
        bottom_layout.addWidget(self.next_button,alignment=Qt.AlignmentFlag.AlignRight| Qt.AlignmentFlag.AlignBottom)

        layout.addLayout(bottom_layout, 1,0, 1,2)


    def update_ui_after_content_drop(self):
        self.correct_files_list.clear()
        self.invalid_files_list.clear()
        for file in self.drop_area.correct_files:
            self.add_file_to_correct_files_list_UI(file, file_is_valid=True)
        for file in self.drop_area.invalid_files:
            self.invalid_files_list.addItem(file)

    def update_current_content_validity(self):
        """Updates status, warnings, and (un)allows the user to proceed to the next step accordingly."""
        num_valid_files = len(self.drop_area.correct_files)
        self.correct_files_label.setText(f"Valid files ({num_valid_files} / {self.main_window.max_files_amount})")
        if num_valid_files >= self.drop_area.min_file_amount:
            self.next_button.setEnabled(True)
            self.status_label.setText("🗸 Ready to analyze 🗸")
            self.status_label.setStyleSheet(("font-size:20px;color:green;"))
        else:
            self.next_button.setEnabled(False)
            self.status_label.setText(f"⚠️ {num_valid_files} valid file{'s' if num_valid_files != 1 else ''} dropped.")
            self.status_label.setStyleSheet(("font-size:20px;color:red"))

    def go_back(self): ##to consider : add a generic method for all "go back" buttons ?
        self.main_window.stacked_widget.setCurrentIndex(0)
        self.main_window.help_window.expand_step(0)

    def _browse_directory(self):
        """Open dialog for selecting a directory."""
        directory_path = QFileDialog.getExistingDirectory(self, "Select a directory with .txt files")
        if directory_path:
            self.drop_area.process_directory(directory_path)
            self.update_ui_after_content_drop()
            self.update_current_content_validity()

    def _browse_single_file(self):
        """Open file dialog for selecting files manually."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .txt file", "", "Text Files (*.txt)")
        if file_name:
            print("Selected file:", file_name)
            if self.drop_area.file_format_is_valid(file_name):
                self.drop_area.correct_files.append(file_name)
                self.add_file_to_correct_files_list_UI(file_name, file_is_valid=True)
                self.update_current_content_validity()
            else:
                pass
                #self.show_warning("Please select only .txt files.")
    def add_file_to_correct_files_list_UI(self, file, file_is_valid=True):
        """
        Adds a given file to its correct list (valid or invalid) only in the UI.
        The addition to a "physical" list is handled in the DropArea class (at ./utilities.py)
        """
        item = QListWidgetItem(self.correct_files_list if file_is_valid else self.invalid_files_list)
        widget = QWidget()
        layout = QHBoxLayout()

        file_label = QLabel(file)
        layout.addWidget(file_label)
        if file_is_valid:
            remove_button = QPushButton("✕")
            remove_button.setStyleSheet("background: none; border: none; color: red; font-weight: bold;")
            remove_button.setFixedSize(20, 20)
            remove_button.clicked.connect(lambda: self.remove_file(file, item, file_is_valid))
            remove_button.setVisible(False)
            layout.addWidget(remove_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        widget.setLayout(layout)
        widget.installEventFilter(self) #is it necessary to do that on each new file added ?

        item.setSizeHint(widget.sizeHint())
        list_widget = self.correct_files_list if file_is_valid else self.invalid_files_list
        list_widget.setItemWidget(item, widget)

    def remove_file(self, file, item, valid=True):
        if valid:
            self.drop_area.correct_files.remove(file) #PROBLEM TODO : access to a public attribute !!
            self.correct_files_list.takeItem(self.correct_files_list.row(item))
        else:
            self.drop_area.invalid_files.remove(file)
            self.invalid_files_list.takeItem(self.invalid_files_list.row(item))
        self.update_current_content_validity()

    @override #override of the default eventFilter provided by PySide6
    def eventFilter(self, watched, event):
        remove_button = watched.findChild(QPushButton)
        #assert(isinstance(remove_button, QPushButton))
        if event.type() == QEvent.Type.Enter:
            if remove_button:
                remove_button.setVisible(True)
        elif event.type() == QEvent.Type.Leave:
            if remove_button:
                remove_button.setVisible(False)
        return super().eventFilter(watched, event)

    def proceed_to_next_step(self):
        #print("Proceeding to step 2 with files:", self.drop_area.correct_files)
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
        self.label.setStyleSheet("font-size:24px;")
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.simple_analysis_radio = sradiobuttons.SRadioButton("Simple Analysis    ")
        self.complex_analysis_radio = sradiobuttons.SRadioButton("Complex Analysis")

        self.analysis_group = QButtonGroup()
        self.analysis_group.addButton(self.simple_analysis_radio)
        self.analysis_group.addButton(self.complex_analysis_radio)

        layout.addWidget(self.simple_analysis_radio, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.complex_analysis_radio, alignment=Qt.AlignmentFlag.AlignCenter)

        self.description_label = QLabel("Select an analysis type to see a brief description.")
        self.description_label.setStyleSheet("font-size:24px;")
        layout.addWidget(self.description_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.launch_button = sbuttons.SButtons("LAUNCH")
        self.launch_button.setEnabled(False)
        self.launch_button.clicked.connect(self.proceed_to_next_step)
        layout.addWidget(self.launch_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.go_back_button = sbuttons.SButtons("Back")
        self.go_back_button.clicked.connect(self._go_back)
        layout.addWidget(self.go_back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.simple_analysis_radio.toggled.connect(self.update_description)
        self.complex_analysis_radio.toggled.connect(self.update_description)

        self.setLayout(layout)

    def _go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(1)
        self.main_window.help_window.expand_step(1)

    def update_description(self):
        if self.simple_analysis_radio.isChecked():
            self.description_label.setText("Simple Analysis: A quick overview of the files.")
            self.launch_button.setEnabled(True)
        elif self.complex_analysis_radio.isChecked():
            self.description_label.setText("Complex Analysis: A detailed and thorough analysis.")
            self.launch_button.setEnabled(True)

    def proceed_to_next_step(self):
        selected_analysis = "simple" if self.simple_analysis_radio.isChecked() else "complex"
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
        self.next_button = sbuttons.SButtons("Next")
        self.analysis_complexity = analysis_complexity

        layout = QVBoxLayout()

        self.current_file_processed_label = QLabel("Processing: None")
        self.current_file_processed_label.setStyleSheet("font-size:24px;")
        layout.addWidget(self.current_file_processed_label)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)

        self.done.connect(lambda: QTimer.singleShot(200, self.move_to_step4))

        self.setLayout(layout)

        self.comparison_content = None
        QTimer.singleShot(70, self._process_files)
    def _process_files(self):
        valid_files_to_process = self.main_window.step1_widget.drop_area.correct_files
        #type = self.main_window.max_files_amount
        if self.main_window.max_files_amount == 1:
            #web scraping, etc
            ...
            print("processing a SINGLE FILE")
            CURRENT_TIME = time()
            self.main_window.final_results = OneFileComparison(self.progress_bar, valid_files_to_process[0], self.analysis_complexity)
            print("OneFileComparison done in", time() - CURRENT_TIME)
        else:
            ...
            print("processing a SET of FILES")
            #compare files between each other
            CURRENT_TIME = time()
            self.main_window.final_results = CrossCompare(self.progress_bar ,files_paths=valid_files_to_process, comparison_type=self.analysis_complexity)
            print("CrossCompare done in", time() - CURRENT_TIME)

        # Mark all as complete
        self.current_file_processed_label.setText("Processing: Complete")
        QTimer.singleShot(100, self.done.emit)


    def move_to_step4(self):
        self.main_window.step4_widget = Step4_DisplayResults(self.main_window)
        self.main_window.stacked_widget.addWidget(self.main_window.step4_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step4_widget)
        self.main_window.help_window.expand_step(4)

class Step4_DisplayResults(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        file_selection_layout = QHBoxLayout()
        self.right_content_title = QComboBox()

        if isinstance(self.main_window.final_results, OneFileComparison):
            #TODO : complete this
            self.left_content_title = QComboBox()
            self.left_content_title.addItem(self.main_window.final_results.source_file)
            items_to_compare_base_with = sorted(list(self.main_window.final_results.comparison_with.keys())) #the site names
            self.right_content_title.addItems(items_to_compare_base_with)
            ...

        elif isinstance(self.main_window.final_results, CrossCompare):
            self.left_content_title = QComboBox()
            self.left_content_title.addItems(self.main_window.step1_widget.drop_area.correct_files)
            items_to_compare_base_with = self.main_window.step1_widget.drop_area.correct_files
            self.right_content_title.addItems(items_to_compare_base_with)
            self.left_content_title.currentIndexChanged.connect(lambda : self._sync_comboboxes(self.left_content_title))
            self.right_content_title.currentIndexChanged.connect(lambda : self._sync_comboboxes(self.right_content_title))
        else:
            raise TypeError("Unexpected type for final_results")

        label = QLabel("File 1:")
        label.setStyleSheet("font-size:24px;")
        file_selection_layout.addWidget(label)
        file_selection_layout.addWidget(self.left_content_title)

        switch_button = QPushButton("Switch Contents")
        switch_button.clicked.connect(self._switch_contents)
        file_selection_layout.addWidget(switch_button)

        label2 = QLabel("File2 :")
        label2.setStyleSheet("font-size:24px;")
        file_selection_layout.addWidget(label2)
        file_selection_layout.addWidget(self.right_content_title)

        layout.addLayout(file_selection_layout)

        self.file1_result_labels = {}
        self.file2_result_labels = {}
        self.common_result_labels = {}

        self.textual_display_common_charcs = COMMON_CHARS_SIMPLE if self.main_window.step3_widget.analysis_complexity == "simple" else COMMON_CHARS_COMPLEX
        self.textual_display_common_func_labels = COMMON_CHARS_SIMPLE_ATTRS if self.main_window.step3_widget.analysis_complexity == "simple" else COMMON_CHARS_COMPLEX_ATTRS

        self.graphical_display_common_charcs = GRAPH_COMMON_CHARS_SIMPLE if self.main_window.step3_widget.analysis_complexity == "simple" else GRAPH_COMMON_CHARS_COMPLEX
        self.graphical_display_common_func_labels = GRAPH_COMMON_CHARS_SIMPLE_ATTRS if self.main_window.step3_widget.analysis_complexity == "simple" else GRAPH_COMMON_CHARS_COMPLEX_ATTRS

        for char in INDIV_CHARACTERISTICS:
            # adding each characteristic specific to each text that way :
            # [char_name]    [file1_char_value]    [file2_char_value]
            char_values_line_layout = QHBoxLayout()

            char_label = QLabel(char)
            char_label.setStyleSheet("font-size:18px")
            common_result_label = QLabel("-")
            common_result_label.setStyleSheet("font-size:18px")
            result2_label = QLabel("-")
            result2_label.setStyleSheet("font-size:18px")

            char_values_line_layout.addWidget(char_label)
            char_values_line_layout.addWidget(common_result_label)
            char_values_line_layout.addWidget(result2_label)

            self.file1_result_labels[char] = common_result_label
            self.file2_result_labels[char] = result2_label

            layout.addLayout(char_values_line_layout)

        for common_char in self.textual_display_common_charcs:
            char_values_line_layout = QHBoxLayout()

            char_label = QLabel(common_char)
            char_label.setStyleSheet("font-size:18px")
            common_result_label = QLabel("-")
            common_result_label.setStyleSheet("font-size:18px")

            char_values_line_layout.addWidget(char_label)
            char_values_line_layout.addWidget(common_result_label)
            self.common_result_labels[common_char] = common_result_label

            layout.addLayout(char_values_line_layout)

        graph_view_button = sbuttons.SButtons("View Graph")
        graph_view_button.clicked.connect(self._view_graph)
        layout.addWidget(graph_view_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.reset_button = sbuttons.SButtons("Reset")
        self.reset_button.clicked.connect(self._reset_process_entirely)
        layout.addWidget(self.reset_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self._sync_comboboxes(self.left_content_title)
        self._sync_comboboxes(self.right_content_title)


    def _reset_process_entirely(self):
        self.main_window.final_results = None
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step0_widget)

    def _update_results(self):
        file1, file2 = self.left_content_title.currentText(), self.right_content_title.currentText()
        results = self.main_window.final_results
        for char_name, char_label in zip(INDIV_CHARACTERISTICS, INDIV_CHARS_ATTRS):
            try:
                res_file1 = getattr(results.content_stats[file1], char_label)
                res_file2 = getattr(results.content_stats[file2], char_label)
            except UnprocessableTextContent:
                pass #TODO : handle this case
                res_file1 = "N/A"
                res_file2 = "N/A"

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

    def _sync_comboboxes(self, changed_combobox):
        selected_item = changed_combobox.currentText()

        if changed_combobox == self.left_content_title:
            target_combobox = self.right_content_title
            items = self.main_window.step1_widget.drop_area.correct_files
        else:
            target_combobox = self.left_content_title
            items = self.main_window.step1_widget.drop_area.correct_files
        target_combobox.blockSignals(True)

        target_combobox.clear()
        for item in items:
            if item != selected_item:
                target_combobox.addItem(item)

        if target_combobox.count() > 0:
            target_combobox.setCurrentIndex(0)

        target_combobox.blockSignals(False)
        self._update_results()


    def _switch_contents(self):
        left_file = self.left_content_title.currentText()
        right_file = self.right_content_title.currentText()
        self.left_content_title.blockSignals(True)
        self.right_content_title.blockSignals(True)

        self.left_content_title.addItem(right_file)
        self.right_content_title.addItem(left_file)
        left_index = self.left_content_title.findText(right_file)
        right_index = self.right_content_title.findText(left_file)

        if left_index != -1:
            self.left_content_title.setCurrentIndex(left_index)
        if right_index != -1:
            self.right_content_title.setCurrentIndex(right_index)

        self.left_content_title.blockSignals(False)
        self.right_content_title.blockSignals(False)
        self._sync_comboboxes(self.left_content_title)
        self._sync_comboboxes(self.right_content_title)

    def _prepare_graphs_data(self):
        file1, file2 = self.left_content_title.currentText(), self.right_content_title.currentText()
        results = self.main_window.final_results
        graphs_data = []

        for char_name, char_label in zip(self.graphical_display_common_charcs, self.graphical_display_common_func_labels):
            res_file1 = getattr(results.content_stats[file1], char_label)
            res_file2 = getattr(results.content_stats[file2], char_label)
            graphs_data.append((char_name, res_file1, res_file2))
        return graphs_data

    def _view_graph(self):
        graphs_data = self._prepare_graphs_data()
        self.graph_window = GraphWindow(self.main_window)

        for graph_name, res_file1, res_file2 in graphs_data:
            if "length" in graph_name:
                freq_dist1 = res_file1
                freq_dist2 = res_file2
                self.graph_window.add_LengthPlot_graph(
                    name=graph_name,
                    lengths1=freq_dist1,
                    lengths2=freq_dist2,
                    x_label="Sentence index",
                    y_label="Length",
                    title=f"{graph_name} Comparison"
                )
            else:
                freq_dist1 = res_file1
                freq_dist2 = res_file2
                self.graph_window.add_FreqDist_graph(
                    name=graph_name,
                    freq_dist1=freq_dist1,
                    freq_dist2=freq_dist2,
                    x_label="Items",
                    y_label="Frequency",
                    title=f"{graph_name} Comparison"
                )

        self.graph_window.show()
        #TODO : fix the logic of this
        #self.left_content_title.currentIndexChanged.connect(self.update_graph_window)
        #self.right_content_title.currentIndexChanged.connect(self.update_graph_window)

    """
    def update_graph_window(self):
        if self.graph_window:
            new_graphs_data = self.prepare_graphs_data()
            for graph_name, res_file1, res_file2 in new_graphs_data:
                freq_dist1 = FreqDist(dict(res_file1))
                freq_dist2 = FreqDist(dict(res_file2))
                self.graph_window.update_FreqDist_graph(
                    name=graph_name,
                    freq_dist1=freq_dist1,
                    freq_dist2=freq_dist2,
                    x_label="Items",
                    y_label="Frequency",
                    title=f"{graph_name} Comparison"
                )
    """
