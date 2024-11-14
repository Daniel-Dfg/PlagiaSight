import re
from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum

from lemminflect import getLemma
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from numpy import array, append, ndarray

from .constants import REGEX_SPLIT_SENTENCES, MAX_TEXT_LEN, CUSTOM_PUNCTUATION
from .exceptions import TokenListIsEmpty, UnprocessableTextContent

class POSTag(Enum):
    ADJ = 'ADJ'
    VERB = 'VERB'
    ADV = 'ADV'
    NOUN = 'NOUN'

@dataclass
class Tokenizer:
    _raw_data: str
    _tokens_by_sentence: ndarray = field(init=False, repr=False)
    _tokens_by_wordpunct: ndarray = field(init=False, repr=False)
    _tokens_by_word: ndarray = field(init=False, repr=False, default_factory=lambda: array([]))
    _tokens_by_syntagm: ndarray = field(init=False, repr=False, default_factory=lambda: array([]))
    _part_of_speeches_tags: ndarray = field(init=False, repr=False, default_factory=lambda: array([]))
    _stop_words: set = field(default_factory=lambda: set(stopwords.words('english')), init=False, repr=False)

    def __post_init__(self):
        # Split raw data into sentences
        self._tokens_by_sentence = self._split_sentences(self._raw_data)
        if len(self._tokens_by_sentence) < MAX_TEXT_LEN:
            raise UnprocessableTextContent("text richness")

        # Tokenize and tag
        tokens_by_wordpunct = wordpunct_tokenize(self._raw_data)
        pos_tags = self._lemmatize_and_tag_tokens(tokens_by_wordpunct)
        self._tokens_by_syntagm, self._tokens_by_wordpunct = self._filter_and_group_tokens(pos_tags)

    def _split_sentences(self, text: str) -> ndarray:
        """Splits text into sentences based on a regular expression."""
        return array([sent.strip() for sent in re.split(REGEX_SPLIT_SENTENCES, text) if sent.strip()])

    def _lemmatize_and_tag_tokens(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """Lemmatizes and tags tokens with POS tags."""
        pos_tagged = pos_tag(tokens)
        # oepsie ik concat >_< (list comprehension)

        # For each (token, tag) in pos_tagged:
        # - If the token is not only punctuation:
        #     - Attempt to lemmatize it using getLemma(token, self.get_tag_lemminflect(tag)):
        #       - getLemma returns a list of possible lemmas (root forms) for the token based on its POS tag
        #       - If a lemma is found, take the first one from the list (getLemma(...)[0])
        #       - If no lemma is found, use the original token itself as the lemmatized form
        #     - The result is a tuple: (lemmatized token or original token, tag)
        # - If the token is only punctuation:
        #     - Mark it with the tag "Punct" to indicate it's punctuation
        # The final output is a list of tuples, each containing a (lemmatized token or punctuation, POS tag)

        return [
            (getLemma(token, self.get_tag_lemminflect(tag))[0] if getLemma(token, self.get_tag_lemminflect(tag)) else token, tag)
            if not self._is_only_punctuation(token) else (token, "Punct")
            for token, tag in pos_tagged
        ]

    def _filter_and_group_tokens(self, pos_tags: List[Tuple[str, str]]) -> Tuple[ndarray, ndarray]:
        """Filters tokens, groups them by syntagm, and assigns POS tags."""
        filtered_tokens = []
        syntagms = []
        current_syntagm = []

        for term, pos in pos_tags:
            if term in self._stop_words or self._is_only_punctuation(term) or term == '':
                if current_syntagm:
                    syntagms.append(current_syntagm)
                    current_syntagm = []
                if self._is_only_punctuation(term):
                    filtered_tokens.append(term)
                    self._part_of_speeches_tags = append(self._part_of_speeches_tags, pos)
            else:
                current_syntagm.append(term)
                filtered_tokens.append(term)
                self._part_of_speeches_tags = append(self._part_of_speeches_tags, pos)
                self._tokens_by_word = append(self._tokens_by_word, term)

        if current_syntagm:
            syntagms.append(current_syntagm)

        return array(syntagms, dtype=object), array(filtered_tokens)

    def _is_only_punctuation(self, token: str) -> bool:
        """Checks if the token consists only of punctuation."""
        return all(char in CUSTOM_PUNCTUATION for char in token)

    def get_tag_lemminflect(self, tag: str) -> str:
        """Maps NLTK POS tags to Lemminflect POS tags."""
        if tag.startswith('J'):
            return POSTag.ADJ.value
        elif tag.startswith('V'):
            return POSTag.VERB.value
        elif tag.startswith('R'):
            return POSTag.ADV.value
        else:
            return POSTag.NOUN.value

    @property
    def tokens_by_sentence(self) -> ndarray:
        return self._check_tokens(self._tokens_by_sentence, "tokens by sentence")

    @property
    def tokens_by_wordpunct(self) -> ndarray:
        return self._check_tokens(self._tokens_by_wordpunct, "tokens by word/punctuation")

    @property
    def tokens_by_word(self) -> ndarray:
        return self._check_tokens(self._tokens_by_word, "tokens by word")

    @property
    def tokens_by_syntagm(self) -> ndarray:
        return self._check_tokens(self._tokens_by_syntagm, "tokens by syntagm")

    @property
    def part_of_speeches(self) -> ndarray:
        return self._check_tokens(self._part_of_speeches_tags, "words' POS tags")

    def _check_tokens(self, tokens: ndarray, attribute_name: str) -> ndarray:
        """Checks if tokens exist, otherwise raises an exception."""
        if not tokens.size:
            raise TokenListIsEmpty(attribute_name)
        return tokens

    @property
    def raw_data(self) -> str:
        if not self._raw_data:
            raise UnprocessableTextContent("raw data")
        return self._raw_data