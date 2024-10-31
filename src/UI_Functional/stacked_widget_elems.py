from PySide6.QtWidgets import (QGridLayout, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
                             QListWidget, QHBoxLayout, QComboBox, QRadioButton,
                             QButtonGroup, QProgressBar, QHBoxLayout, QListWidgetItem)
from PySide6.QtCore import Qt, QTimer, Signal, QEvent
from nltk.metrics.aline import align
from TextAnalysis import UnprocessableTextContent
from .comparison_results import OneFileComparison, CrossCompare
from nltk import FreqDist
from .utilities import DropArea, GraphWindow
from UI_Styling import slabels, sbuttons, filescontainer
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

        #Set Labels
        for label,font_size in labels.items():
            label.setStyleSheet(f"font-size: {font_size}px;")
            layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Buttons
        button1 = sbuttons.SButtons("One file with related online data")
        button2 = sbuttons.SButtons("A set of files between each other")

        # Buttons Functionalities
        buttons = {button1: (lambda: self.proceed_to_step1(1)), button2: (lambda: self.proceed_to_step1(MAX_FILES_AMOUNT))}

        # Set Buttons
        for button, func in buttons.items():
            button.clicked.connect(func)
            button.setFixedSize(280, 50)
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)


        self.setLayout(layout)

    def proceed_to_step1(self, max_files_amount):
        self.main_window.max_files_amount = max_files_amount
        self.main_window.step1_widget = Step1_FileDropAndCheck(self.main_window)
        self.main_window.stacked_widget.addWidget(self.main_window.step1_widget)
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step1_widget)
        self.main_window.help_window.expand_step(1)


class Step1_FileDropAndCheck(QWidget):
    def __init__(self, main_window):
        super().__init__()
        # Main layout
        self.main_window = main_window
        layout = QGridLayout(self)

        # Drop Area
        self.drop_area = DropArea(self, self.main_window.max_files_amount)
        layout.addWidget(self.drop_area,0,0, alignment=Qt.AlignmentFlag.AlignCenter |Qt.AlignmentFlag.AlignLeft)

        # Browse Buttons
        self.drop_area.browseFiles.clicked.connect(self.open_file_dialog)
        if self.main_window.max_files_amount == MAX_FILES_AMOUNT:
            self.drop_area.browseFolders.setDisabled(False)
            self.drop_area.browseFolders.setHidden(False)
            self.drop_area.browseFolders.clicked.connect(self.open_directory_dialog)

        # Files container
        self.filesContainers = filescontainer.FilesContainer()
        self.correct_files_label = self.filesContainers.validContainer.label
        self.correct_files_label.setText(f"Valid files (0 / {self.main_window.max_files_amount})")
        self.invalid_files_label = self.filesContainers.validContainer.label
        self.correct_files_list = self.filesContainers.validContainer.container
        self.invalid_files_list = self.filesContainers.invalidContainer.container
        layout.addWidget(self.filesContainers, 0,1)

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        self.back_button = sbuttons.SButtons("Back")
        self.back_button.clicked.connect(self.go_back)
        bottom_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.status_label = QLabel("Nothing dropped yet!")
        self.status_label.setStyleSheet("font-size:20px;color:white;")
        bottom_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.next_button = sbuttons.SButtons("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.proceed_to_step2)
        bottom_layout.addWidget(self.next_button,alignment=Qt.AlignmentFlag.AlignRight| Qt.AlignmentFlag.AlignBottom)

        layout.addLayout(bottom_layout, 1,0, 1,2)


    def update_ui_after_drop(self):
        self.correct_files_list.clear()
        self.invalid_files_list.clear()
        for file in self.drop_area.correct_files:
            self.add_file_to_list_viz(file, valid=True)
        for file in self.drop_area.invalid_files:
            self.invalid_files_list.addItem(file)

    def update_status(self):
        """Update status based on the number of files dropped."""
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

    def go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(0)
        self.main_window.help_window.expand_step(0)

    def open_directory_dialog(self):
        """Open dialog for selecting a directory."""
        options = QFileDialog.Options()
        directory_path = QFileDialog.getExistingDirectory(self, "Select a directory with .txt files", options=options)
        if directory_path:
            self.drop_area.process_directory(directory_path)
            self.update_ui_after_drop()
            self.update_status()
    def open_file_dialog(self):
        """Open file dialog for selecting files manually."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .txt file or a directory", "", "Text Files (*.txt)")
        if file_name:
            print("Selected file:", file_name)
            if self.drop_area.is_valid_format_file(file_name):
                self.drop_area.correct_files.append(file_name)
                self.add_file_to_list_viz(file_name, valid=True)
                self.update_status()
            else:
                self.show_warning("Please select only .txt files.")
    def add_file_to_list_viz(self, file, valid=True):
        """
        TODO (top priority) : change the logic of file addition
        (e.g make an alternative to addItem without overriding to add an item with an hover + delete method,
        put that in step1 widget)
        """
        item = QListWidgetItem(self.correct_files_list if valid else self.invalid_files_list)

        # Crée un widget pour afficher le chemin du fichier et un bouton pour le retirer
        widget = QWidget()
        layout = QHBoxLayout()

        file_label = QLabel(file)
        layout.addWidget(file_label)
        if valid:
            remove_button = QPushButton("✕")
            remove_button.setStyleSheet("background: none; border: none; color: red; font-weight: bold;")
            remove_button.setFixedSize(20, 20)
            remove_button.clicked.connect(lambda: self.remove_file(file, item, valid))
            remove_button.setVisible(False)
            layout.addWidget(remove_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        widget.setLayout(layout)
        widget.installEventFilter(self)

        item.setSizeHint(widget.sizeHint())
        list_widget = self.correct_files_list if valid else self.invalid_files_list
        list_widget.setItemWidget(item, widget)

    def remove_file(self, file, item, valid=True):
        if valid:
            self.drop_area.correct_files.remove(file)
            self.correct_files_list.takeItem(self.correct_files_list.row(item))
        else:
            self.drop_area.invalid_files.remove(file)
            self.invalid_files_list.takeItem(self.invalid_files_list.row(item))
        self.update_status()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            remove_button = obj.findChild(QPushButton)
            if remove_button:
                remove_button.setVisible(True)
        elif event.type() == QEvent.Type.Leave:
            remove_button = obj.findChild(QPushButton)
            if remove_button:
                remove_button.setVisible(False)
        return super().eventFilter(obj, event)

    def proceed_to_step2(self):
        """Proceed to the next step with the files."""
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

        self.launch_button = sbuttons.SButtons("LAUNCH")
        self.launch_button.setEnabled(False)
        self.launch_button.clicked.connect(self.launch_analysis)
        layout.addWidget(self.launch_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.go_back_button = sbuttons.SButtons("Back")
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
        layout.addWidget(self.current_file_processed_label)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)

        self.done.connect(lambda: QTimer.singleShot(300, self.move_to_step4))

        self.setLayout(layout)

        self.comparison_content = None
        QTimer.singleShot(100, self.process_files)
        #self.process_files()

    def process_files(self):
        content = self.main_window.step1_widget.drop_area.correct_files
        #type = self.main_window.max_files_amount
        if self.main_window.max_files_amount == 1:
            #web scraping, etc
            ...
            print("processing a SINGLE FILE")
            CURRENT_TIME = time()
            self.main_window.final_results = OneFileComparison(self.progress_bar, content[0], self.analysis_complexity)
            print("OneFileComparison done in", time() - CURRENT_TIME)
        else:
            ...
            print("processing a SET of FILES")
            #compare files between each other
            CURRENT_TIME = time()
            self.main_window.final_results = CrossCompare(self.progress_bar ,files_paths=content, comparison_type=self.analysis_complexity)
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

        graph_view_button = QPushButton("View Graph")
        graph_view_button.clicked.connect(self.view_graph)
        layout.addWidget(graph_view_button, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Comparison Results")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        file_selection_layout = QHBoxLayout()
        self.right_content_title = QComboBox()

        if isinstance(self.main_window.final_results, OneFileComparison):
            #TODO : complete this
            self.left_content_title = QComboBox()
            self.left_content_title.addItem(self.main_window.final_results.source_file)
            right_items = sorted(list(self.main_window.final_results.comparison_with.keys())) #the site names
            self.right_content_title.addItems(right_items)
        elif isinstance(self.main_window.final_results, CrossCompare):
            self.left_content_title = QComboBox()
            self.left_content_title.addItems(self.main_window.step1_widget.drop_area.correct_files)
            right_items = self.main_window.step1_widget.drop_area.correct_files
            self.right_content_title.addItems(right_items)
            self.left_content_title.currentIndexChanged.connect(lambda : self.sync_comboboxes(self.left_content_title))
            self.right_content_title.currentIndexChanged.connect(lambda : self.sync_comboboxes(self.right_content_title))


        else:
            raise TypeError("Unexpected type for final_results")

        file_selection_layout.addWidget(QLabel("File 1:"))
        file_selection_layout.addWidget(self.left_content_title)
        switch_button = QPushButton("Switch Files")
        switch_button.clicked.connect(self.switch_files)
        file_selection_layout.addWidget(switch_button)
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

        for common_char in self.textual_display_common_charcs:
            line_layout = QHBoxLayout()

            char_label = QLabel(common_char)
            common_result_label = QLabel("-")

            line_layout.addWidget(char_label)
            line_layout.addWidget(common_result_label)
            self.common_result_labels[common_char] = common_result_label

            layout.addLayout(line_layout)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_process_entirely)
        layout.addWidget(self.reset_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.sync_comboboxes(self.left_content_title)
        self.sync_comboboxes(self.right_content_title)


    def reset_process_entirely(self):
        self.main_window.final_results = None
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.step0_widget)

    def update_results(self):
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


    def sync_comboboxes(self, changed_combobox):
        # Récupère l'élément actuellement sélectionné dans la combobox qui a changé
        selected_item = changed_combobox.currentText()

        # Détermine quelle combobox doit être mise à jour (l'autre combobox)
        if changed_combobox == self.left_content_title:
            target_combobox = self.right_content_title
            items = self.main_window.step1_widget.drop_area.correct_files
        else:
            target_combobox = self.left_content_title
            items = self.main_window.step1_widget.drop_area.correct_files
        target_combobox.blockSignals(True)

        # Efface la combobox cible et ajoute les éléments en excluant l'élément sélectionné
        target_combobox.clear()
        for item in items:
            if item != selected_item:
                target_combobox.addItem(item)

        # Réinitialise l'index pour éviter des erreurs si l'autre combobox n'a qu'un seul élément restant
        if target_combobox.count() > 0:
            target_combobox.setCurrentIndex(0)

        target_combobox.blockSignals(False)
        self.update_results()


    def switch_files(self):
        # Sauvegarder les éléments sélectionnés
        left_file = self.left_content_title.currentText()
        right_file = self.right_content_title.currentText()
        self.left_content_title.blockSignals(True)
        self.right_content_title.blockSignals(True)

        self.left_content_title.addItem(right_file)
        self.right_content_title.addItem(left_file)

        # Changer les éléments sélectionnés
        left_index = self.left_content_title.findText(right_file)
        right_index = self.right_content_title.findText(left_file)

        if left_index != -1:
            self.left_content_title.setCurrentIndex(left_index)
        if right_index != -1:
            self.right_content_title.setCurrentIndex(right_index)

        # Mettre à jour les résultats après le switch
        self.left_content_title.blockSignals(False)
        self.right_content_title.blockSignals(False)
        self.sync_comboboxes(self.left_content_title)
        self.sync_comboboxes(self.right_content_title)

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
        if self.graph_window:  # Vérifiez si la fenêtre du graphique est déjà ouverte
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
