from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, Tuple, Union, Counter, TypeVar

from nltk import FreqDist

from .tsar import TokensStatsAndRearrangements

T = TypeVar('T', Tuple[str, str], Tuple[str, str, str])

@dataclass
class TokensComparisonAlgorithms:
    """Calculates and caches similarity metrics between token sets on demand for modularity."""
    _input_tokens_sets: TokensStatsAndRearrangements
    _source_tokens_sets: TokensStatsAndRearrangements
    _similarity_cache: Dict[str, float] = field(init=False, default_factory=dict)
    _all_term_frequencies: Dict[str, float] = field(init=False, default_factory=dict)
    _identical_bigrams: Dict[Tuple[str, str], Tuple[int, int]] = field(init=False, default_factory=dict)
    _identical_trigrams: Dict[Tuple[str, str, str], Tuple[int, int]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        pass

    def _cosine_similarity(self, source_terms: FreqDist, input_terms: FreqDist) -> float:
        input_norm = sqrt(sum(value ** 2 for value in input_terms.values()))
        source_norm = sqrt(sum(value ** 2 for value in source_terms.values()))

        if input_norm == 0 or source_norm == 0:
            return 0.0

        dot_product = sum(source_terms.get(word, 0) * input_terms.get(word, 0) for word in set(source_terms) | set(input_terms))

        return dot_product / (input_norm * source_norm)

    def _jaccard_similarity(self, source_terms: set, input_terms: set) -> float:
        union_size = len(source_terms | input_terms)

        if union_size == 0:
            return 0.0

        return len(source_terms & input_terms) / union_size

    def _compute_similarity(self, sim_type: str, token_type: str) -> float:
        cache_key = f"{sim_type}_{token_type}"

        if cache_key in self._similarity_cache:
            return self._similarity_cache[cache_key]

        if token_type == "words":
            source_terms = self._source_tokens_sets.word_freq
            input_terms = self._input_tokens_sets.word_freq
        elif token_type == "pos":
            source_terms = self._source_tokens_sets.pos_freq
            input_terms = self._input_tokens_sets.pos_freq
        else:
            raise ValueError("Invalid token type. Must be 'words' or 'pos'.")

        if sim_type == "cosine":
            result = self._cosine_similarity(source_terms, input_terms)
        elif sim_type == "jaccard":
            result = self._jaccard_similarity(set(source_terms), set(input_terms))
        else:
            raise ValueError("Invalid similarity type. Must be 'cosine' or 'jaccard'.")

        self._similarity_cache[cache_key] = result
        return result

    @property
    def input_tokens_sets(self):
        return self._input_tokens_sets

    @property
    def source_tokens_sets(self):
        return self._source_tokens_sets

    @property
    def all_term_frequencies(self) -> Dict[str, float]:
        if not self._all_term_frequencies:
            all_terms = set(self._input_tokens_sets.word_freq) | set(self._source_tokens_sets.word_freq)
            self._all_term_frequencies = {term: self._input_tokens_sets.word_freq.get(term, 0) + self._source_tokens_sets.word_freq.get(term, 0)
                                          for term in all_terms}
        return self._all_term_frequencies

    @property
    def cosine_sim_words(self) -> float:
        return self._compute_similarity("cosine", "words")

    @property
    def jaccard_sim_words(self) -> float:
        return self._compute_similarity("jaccard", "words")

    @property
    def cosine_sim_pos(self) -> float:
        return self._compute_similarity("cosine", "pos")

    @property
    def jaccard_sim_pos(self) -> float:
        return self._compute_similarity("jaccard", "pos")

    def find_similar_ngrams(self, input_ngrams: Union[FreqDist, Counter], source_ngrams: Union[FreqDist, Counter]) -> Dict[T, Tuple[int, int]]:
        return {ngram: (input_ngrams[ngram], source_ngrams[ngram]) for ngram in input_ngrams if ngram in source_ngrams}

    @property
    def similar_bigrams(self) -> Dict[Tuple[str, str], Tuple[int, int]]:
        if not self._identical_bigrams:
            self._identical_bigrams = self.find_similar_ngrams(
                self._input_tokens_sets.bigrams,
                self._source_tokens_sets.bigrams
            )
        return self._identical_bigrams

    @property
    def similar_trigrams(self) -> Dict[Tuple[str, str, str], Tuple[int, int]]:
        if not self._identical_trigrams:
            self._identical_trigrams = self.find_similar_ngrams(
                self._input_tokens_sets.trigrams,
                self._source_tokens_sets.trigrams
            )
        return self._identical_trigrams