from TextAnalysis_AkaPhase1 import Tokenizer, TokensComparisonAlgorithms, TokensStatsAndRearrangements, extract_raw_from_file, dataclass, field
from WebScraper import URLs, HtmlText
from PySide6.QtWidgets import QProgressBar


@dataclass
class OneFileComparison:
    """
    - Used when 1 file is provided (step 0)
    - In charge of web scraping and analysis with the resulting texts.
    """
    progress_bar : QProgressBar
    source_file : str # file path
    comparison_type : str # either "simple" or "complex"
    content_stats : dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False, default_factory=dict) #dict[site_name, TSAR]
    comparison_with : dict[str, TokensComparisonAlgorithms] = field(init=False, repr=False, default_factory=dict) #dict[site_name, TPA]

    def __post_init__(self):
        #TODO : make this more explicit

        self.content_stats[self.source_file] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file(self.source_file)))
        source_file_keywords = {k: v for k, v in sorted(self.content_stats[self.source_file].syntagms_scores.items(), key=lambda item: item[1], reverse=True)[:1]}
        print(source_file_keywords.keys())
        for keyword in source_file_keywords.keys():
            u = URLs(keyword, 1)
            associated_urls = u.response_array
            for response in associated_urls:
                site_name = response.url
                text = HtmlText(response)
                self.content_stats[site_name] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file("temp.txt")))
                self.comparison_with[site_name] = TokensComparisonAlgorithms(self.content_stats[self.source_file], self.content_stats[site_name])
                text.removeTempText()
        #links = get_links_from_keywords(self.source_data.base.find_keywords()) (pseudocode)
        #for link in links:
            #self.online_data[link] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_link(text)))
            #self.comparison_with[link] = TextProcessingAlgorithms(self.source_data, self.online_data[link])
        ...
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
    progress_bar : QProgressBar
    files_paths: list[str]
    comparison_type: str  # either "simple" or "complex"
    content_stats: dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False)  # Statistiques individuelles par fichier
    comparisons: dict[tuple[str, str], TokensComparisonAlgorithms] = field(init=False, repr=False)  # Comparaisons entre les fichiers

    def __post_init__(self):
        progress_bar_small_increment = int(30 / (len(self.files_paths)) - 4)
        progress_bar_big_increment = int(70 / (len(self.files_paths)) - 4)
        self.content_stats = {}
        self.comparisons = {}
        if self.comparison_type not in ["simple", "complex"]:
            raise ValueError(f"Invalid comparison type. Must be either 'simple' or 'complex'. It is currently {self.comparison_type}.")

        # Générer les statistiques pour chaque fichier
        #print(self.files_paths, "FILES PATHS")
        self.progress_bar.setValue(0)
        for file in self.files_paths:
            self.content_stats[file] = TokensStatsAndRearrangements(Tokenizer(extract_raw_from_file(file)))
            self.progress_bar.setValue(self.progress_bar.value() + progress_bar_small_increment)

        # Comparer chaque fichier avec les autres
        for i, file1 in enumerate(self.files_paths):
            for j, file2 in enumerate(self.files_paths):
                if i < j:
                    tsar1 = self.content_stats[file1]
                    tsar2 = self.content_stats[file2]
                    self.comparisons[(file1, file2)] = TokensComparisonAlgorithms(tsar1, tsar2)
                    if self.comparison_type == "simple":
                        self.simple_analysis_two_files(file1, file2)
                        #self.comparisons[(file1, file2)].display_simple_results()
                    elif self.comparison_type == "complex":
                        self.complex_analysis_two_files(file1, file2)
                        #self.comparisons[(file1, file2)].display_complex_results()
                    #print("increment by", progress_bar_big_increment)
                    self.progress_bar.setValue(self.progress_bar.value() + progress_bar_big_increment)
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
