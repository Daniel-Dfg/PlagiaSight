from .utilities import simplify_path
from text_analysis import Tokenizer, TokensComparisonAlgorithms, TokensStatsAndRearrangements, extract_raw_from_file, dataclass, field
from web_scraper import URLs, HtmlText
from PySide6.QtWidgets import QLabel, QProgressBar
from PySide6.QtCore import QTimer
import os # to get the file format
#from time import time

#NOTE : the OneFileComparison and CrossCompare classes share (too) many things in common, they could benefit from being grouped into a single class (with eventual derivatives)

#CURRENT_TIME = time()
GATHERED_URLS = 2

@dataclass
class OneFileComparison:
    """
    - Used when 1 file is provided (step 0)
    - In charge of web scraping and analysis with the resulting texts.
    """
    current_status_label : QLabel
    progress_bar : QProgressBar
    source_file : str # file path
    comparison_type : str # either "simple" or "complex"
    problematic_files : list[tuple[str, Exception]] = field(init=False, repr=False, default_factory=list)
    content_stats : dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False, default_factory=dict) #dict[site_name, TSAR]
    comparison_with : dict[str, TokensComparisonAlgorithms] = field(init=False, repr=False, default_factory=dict) #dict[site_name, TPA]

    def __post_init__(self):
        #TODO : make this more explicit
        QTimer.singleShot(80, lambda : self.current_status_label.setText("Processing source file..."))
        progress_bar_small_increment = 15
        progress_bar_big_increment = 30
        file_format = os.path.splitext(self.source_file)[1][1:]
        try:
            self.content_stats[self.source_file] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file(self.source_file, file_format)))
        except Exception as e:
            self.problematic_files.append((self.source_file, e))
            return #bad practice...
        self.current_status_label.setText("Extracting keywords from source text...")
        source_file_keywords = {k: v for k, v in sorted(self.content_stats[self.source_file].syntagms_scores.items(), key=lambda item: item[1], reverse=True)[:1]}

        for keyword in source_file_keywords.keys():
            self.current_status_label.setText("Gathering URLs for the extracted keywords,\n this can take some time...")
            u = URLs(keyword, GATHERED_URLS)
            associated_urls = u.response_array
            self.current_status_label.setText(f"Found the necessary URLs !")
            self.progress_bar.setValue(self.progress_bar.value() + progress_bar_big_increment)
            for response in associated_urls:
                site_name = response.url
                text = HtmlText(response).makeTempText()
                self.current_status_label.setText(f"Computing similarity values between source file and {site_name}")
                try:
                    self.content_stats[site_name] = TokensStatsAndRearrangements(Tokenizer(text))
                    self.comparison_with[site_name] = TokensComparisonAlgorithms(self.content_stats[self.source_file], self.content_stats[site_name])
                except Exception as e:
                    self.problematic_files.append((site_name, e))
                self.progress_bar.setValue(self.progress_bar.value() + progress_bar_small_increment)

    def get_comparison(self, to_be_compared: str) -> TokensComparisonAlgorithms:
        if to_be_compared in self.comparison_with:
            return self.comparison_with[to_be_compared]
        else:
            raise ValueError("The comparison between these files does not exist.")


@dataclass
class CrossCompare:
    """
    Used when a directory is provided (step 0).
    Compares the given files between eachother.
    """
    current_file_processed_label : QLabel
    progress_bar : QProgressBar
    files_paths: list[str]
    comparison_type: str  # either "simple" or "complex"
    problematic_files : list[tuple[str, Exception]] = field(init=False, repr=False, default_factory=list)
    content_stats: dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False)
    comparisons: dict[tuple[str, str], TokensComparisonAlgorithms] = field(init=False, repr=False)

    def __post_init__(self):
        progress_bar_small_increment = int(30 / (len(self.files_paths)) - 4)
        progress_bar_big_increment = int(70 / (len(self.files_paths)) - 4)
        self.content_stats = {}
        self.comparisons = {}
        if self.comparison_type not in ["simple", "complex"]:
            raise ValueError(f"Invalid comparison type. Must be either 'simple' or 'complex'. It is currently {self.comparison_type}.")
            #hello

        self.progress_bar.setValue(0)
        #CURRENT_TIME = time()
        file_counter = 1
        for file in self.files_paths: #Linear treatment, could benefit from parallelization
            simplified_path = simplify_path(file)
            file_format = os.path.splitext(file)[1][1:]
            self.current_file_processed_label.setText(f"Processing {simplified_path} ({file_counter}/{len(self.files_paths)})")
            try:
                self.content_stats[simplified_path] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file(file, file_format))) #BOTTLENECK
            except Exception as e:
                self.problematic_files.append((simplified_path, e))
            self.progress_bar.setValue(self.progress_bar.value() + progress_bar_small_increment)
            file_counter += 1
        #print("Stats generation time:", time() - CURRENT_TIME)

        if self.problematic_files: #bad practice...
            return

        #CURRENT_TIME = time()
        for i, file1 in enumerate(self.files_paths):
            for j, file2 in enumerate(self.files_paths):
                if i < j:
                    simplified_path1, simplified_path2 = simplify_path(file1), simplify_path(file2)
                    tsar1 = self.content_stats[simplified_path1]
                    tsar2 = self.content_stats[simplified_path2]
                    self.comparisons[(simplified_path1, simplified_path2)] = TokensComparisonAlgorithms(tsar1, tsar2)
                    if self.comparison_type == "simple":
                        self.simple_analysis_two_files(simplified_path1, simplified_path2)
                        #self.comparisons[(file1, file2)].display_simple_results()
                    elif self.comparison_type == "complex":
                        self.complex_analysis_two_files(simplified_path1, simplified_path2)
                        #self.comparisons[(file1, file2)].display_complex_results()
                    #print("increment by", progress_bar_big_increment)
                    self.progress_bar.setValue(self.progress_bar.value() + progress_bar_big_increment)
        #print("Comparisons generation time:", time() - CURRENT_TIME)
        self.progress_bar.setValue(100)

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

    def get_comparison(self, file1: str, file2: str) -> TokensComparisonAlgorithms:
        if (file1, file2) in self.comparisons:
            return self.comparisons[(file1, file2)]
        elif (file2, file1) in self.comparisons:
            return self.comparisons[(file2, file1)]
        else:
            raise ValueError("The comparison between these files does not exist.")
