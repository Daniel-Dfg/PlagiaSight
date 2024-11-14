import os
from dataclasses import dataclass, field
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QProgressBar

from .utilities import simplify_path
from Text_Analysis import Tokenizer, TokensComparisonAlgorithms, TokensStatsAndRearrangements, extract_raw_from_file
from Web_Scraper import URLs, HTMLText

GATHERED_URLS = 2

@dataclass
class OneFileComparison:
    current_status_label: QLabel
    progress_bar: QProgressBar
    source_file: str
    comparison_type: str
    problematic_files: list[tuple[str, Exception]] = field(init=False, repr=False, default_factory=list)
    content_stats: dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False, default_factory=dict)
    comparison_with: dict[str, TokensComparisonAlgorithms] = field(init=False, repr=False, default_factory=dict)

    def __post_init__(self):
        QTimer.singleShot(80, lambda: self.current_status_label.setText("Processing source file..."))
        self._process_source_file()
        if self.problematic_files:
            return

        self._gather_urls_for_keywords()

    def _process_source_file(self):
        file_format = os.path.splitext(self.source_file)[1][1:]
        try:
            tokenizer = Tokenizer(extract_raw_from_file(self.source_file, file_format))
            self.content_stats[self.source_file] = TokensStatsAndRearrangements(tokenizer)
        except Exception as e:
            self.problematic_files.append((self.source_file, e))

    def _gather_urls_for_keywords(self):
        source_keywords = sorted(self.content_stats[self.source_file].syntagms_scores.items(), key=lambda item: item[1], reverse=True)[:1]
        for keyword, _ in source_keywords:
            self.current_status_label.setText("Gathering URLs for keywords, this may take some time...")
            urls = URLs(keyword, GATHERED_URLS).response_array
            self.progress_bar.setValue(self.progress_bar.value() + 30)
            self._process_urls(urls)

    def _process_urls(self, urls):
        for response in urls:
            site_name = response.url
            try:
                text = HTMLText(response).makeTempText()
                tokenizer = Tokenizer(text)
                tsar_site = TokensStatsAndRearrangements(tokenizer)
                self.content_stats[site_name] = tsar_site
                self.comparison_with[site_name] = TokensComparisonAlgorithms(self.content_stats[self.source_file], tsar_site)
                self._increment_progress(15)
            except Exception as e:
                self.problematic_files.append((site_name, e))

    def get_comparison(self, to_be_compared: str) -> TokensComparisonAlgorithms:
        if to_be_compared in self.comparison_with:
            return self.comparison_with[to_be_compared]
        else:
            raise ValueError("The comparison between these files does not exist.")

    def _increment_progress(self, amount: int):
        self.progress_bar.setValue(self.progress_bar.value() + amount)


@dataclass
class CrossCompare:
    current_file_processed_label: QLabel
    progress_bar: QProgressBar
    files_paths: list[str]
    comparison_type: str
    problematic_files: list[tuple[str, Exception]] = field(init=False, repr=False, default_factory=list)
    content_stats: dict[str, TokensStatsAndRearrangements] = field(init=False, repr=False)
    comparisons: dict[tuple[str, str], TokensComparisonAlgorithms] = field(init=False, repr=False)

    def __post_init__(self):
        if self.comparison_type not in ["simple", "complex"]:
            raise ValueError(f"Invalid comparison type. Must be either 'simple' or 'complex'. It is currently {self.comparison_type}.")
        self.progress_bar.setValue(0)
        self._process_files()
        if self.problematic_files:
            return
        self._compare_files()

    def _process_files(self):
        for i, file in enumerate(self.files_paths, start=1):
            simplified_path = simplify_path(file)
            file_format = os.path.splitext(file)[1][1:]
            self.current_file_processed_label.setText(f"Processing {simplified_path} ({i}/{len(self.files_paths)})")
            try:
                tokenizer = Tokenizer(extract_raw_from_file(file, file_format))
                self.content_stats[simplified_path] = TokensStatsAndRearrangements(tokenizer)
                self._increment_progress(int(30 / len(self.files_paths)))
            except Exception as e:
                self.problematic_files.append((simplified_path, e))

    def _compare_files(self):
        for i, file1 in enumerate(self.files_paths):
            for j, file2 in enumerate(self.files_paths):
                if i < j:
                    path1, path2 = simplify_path(file1), simplify_path(file2)
                    tsar1, tsar2 = self.content_stats[path1], self.content_stats[path2]
                    self.comparisons[(path1, path2)] = TokensComparisonAlgorithms(tsar1, tsar2)
                    if self.comparison_type == "simple":
                        self.simple_analysis_two_files(path1, path2)
                    else:
                        self.complex_analysis_two_files(path1, path2)
                    self._increment_progress(int(70 / (len(self.files_paths) * (len(self.files_paths) - 1) / 2)))

        self.progress_bar.setValue(100)

    def simple_analysis_two_files(self, file1: str, file2: str) -> None:
        comp = self.comparisons[(file1, file2)]
        _ = comp.cosine_sim_words, comp.jaccard_sim_words

    def complex_analysis_two_files(self, file1: str, file2: str) -> None:
        self.simple_analysis_two_files(file1, file2)
        comp = self.comparisons[(file1, file2)]
        _ = comp.cosine_sim_pos, comp.jaccard_sim_pos

    def get_comparison(self, file1: str, file2: str) -> TokensComparisonAlgorithms:
        if (file1, file2) in self.comparisons:
            return self.comparisons[(file1, file2)]
        elif (file2, file1) in self.comparisons:
            return self.comparisons[(file2, file1)]
        else:
            raise ValueError("The comparison between these files does not exist.")

    def _increment_progress(self, amount: int):
        self.progress_bar.setValue(self.progress_bar.value() + amount)