from collections import Counter, defaultdict
from dataclasses import dataclass, field
from numpy import median
from nltk import FreqDist
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from typing import Dict, List

from .tokenizer import Tokenizer
from .exceptions import UnprocessableTextContent
from .constants import MAX_SENT_LEN

@dataclass
class TokensStatsAndRearrangements:
    _base: Tokenizer
    _bigrams: Counter = field(init=False)
    _trigrams: Counter = field(init=False)
    _word_freq: FreqDist = field(init=False)
    _pos_freq: FreqDist = field(init=False)
    _text_richness: float = field(init=False)
    _sent_lengths: List[int] = field(init=False)
    _average_sent_length: float = field(init=False)
    _median_sent_length: float = field(init=False)
    _syntagms_scores: Dict[str, float] = field(init=False, default_factory=dict)

    def __post_init__(self):
        # Calculate bigrams, trigrams, word frequencies, and POS frequencies
        self._bigrams = Counter(ngrams(self._base.tokens_by_word, 2))
        self._trigrams = Counter(ngrams(self._base.tokens_by_word, 3))
        self._word_freq = FreqDist(self._base.tokens_by_word)
        self._pos_freq = FreqDist(self._base.part_of_speeches)

        # Calculate text richness
        unique_words = set(self._base.tokens_by_word)
        self._text_richness = len(self._base.tokens_by_word) / len(unique_words) if unique_words else 0

        # Calculate sentence lengths and validate average length
        self._sent_lengths = [len(word_tokenize(sent)) for sent in self._base.tokens_by_sentence]
        self._average_sent_length = sum(self._sent_lengths) / len(self._sent_lengths)
        if self._average_sent_length < MAX_SENT_LEN:
            raise UnprocessableTextContent("average sentence length below minimum threshold")

        self._median_sent_length = float(median(self._sent_lengths))

    def evaluate_syntagms_scores(self) -> Dict[str, float]:
        if not self._syntagms_scores:
            # Calculate word degrees for RAKE scoring
            word_degrees = defaultdict(int)

            for syntagm in self._base.tokens_by_syntagm:
                degree = len(syntagm) - 1
                for word in syntagm:
                    word_degrees[word] += degree

            # Calculate word scores
            words_scores = {word: word_degrees[word] / self._word_freq[word] for word in self._word_freq}

            # Assign scores to syntagms
            self._syntagms_scores = {' '.join(syntagm): sum(words_scores.get(word, 0) for word in syntagm)
                                     for syntagm in self._base.tokens_by_syntagm}
        return self._syntagms_scores

    def _check_content(self, content, attribute_name: str):
        if not content:
            raise UnprocessableTextContent(f"{attribute_name} is empty or unprocessable.")
        return content

    @property
    def base(self) -> Tokenizer:
        return self._base

    @property
    def bigrams(self) -> Counter:
        return self._check_content(self._bigrams, "bigrams")

    @property
    def trigrams(self) -> Counter:
        return self._check_content(self._trigrams, "trigrams")

    @property
    def word_freq(self) -> FreqDist:
        return self._word_freq

    @property
    def pos_freq(self) -> FreqDist:
        return self._pos_freq

    @property
    def text_richness(self) -> float:
        return self._check_content(self._text_richness, "text richness")

    @property
    def sent_lengths(self) -> List[int]:
        return self._sent_lengths

    @property
    def average_sent_length(self) -> float:
        return self._average_sent_length

    @property
    def median_sent_length(self) -> float:
        return self._median_sent_length

    @property
    def syntagms_scores(self) -> Dict[str, float]:
        return self.evaluate_syntagms_scores()