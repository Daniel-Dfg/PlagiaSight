"""
By Luckyyyin and Daniel-Dfg
"""

from string import punctuation # helps to check if a string is made of punctuation only here
from math import sqrt
from numpy import array, append
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist, pos_tag
from dataclasses import dataclass, field
from os import path
from collections import Counter
from nltk.util import ngrams


@dataclass
class Tokenizer:
    """
    -> Extracts and Tokenizes data from source
    --> Cleans the data to make it analyzable

    - contains the tokenization methods and the tokens themselves (using @property)
    """
    file: str
    _raw_data: str = field(init=False, repr=False)
    _tokens_by_sentence: array = field(init=False, repr=False)
    _tokens_by_wordpunct: array = field(init=False,  repr=False)
    _tokens_by_word: array = field(init=False, repr=False)

    def __post_init__(self):
        self.extract_raw_from_file()
        self.tokenize_text()
        self.clean_data()

    def extract_raw_from_file(self):
        if not path.exists(self.file):
            raise FileNotFoundError("Specified file doesn't exist")
        with open(self.file, 'r', encoding='utf-8-sig') as f:
            self._raw_data = f.read().lower()

    def tokenize_text(self):
        self._tokens_by_sentence = array(self.raw_data.replace('\n', 'þ').replace('.', 'þ').split('þ'))
        self._tokens_by_wordpunct = array(wordpunct_tokenize(self.raw_data))
        self._tokens_by_word = array([])  # will be created after tokens by wordpunct curation

    def clean_data(self):
        lemmatizer = WordNetLemmatizer()

        # removing stop words and empty tokens
        stop_words = set(stopwords.words('english'))
        self._tokens_by_wordpunct = array([token for token in self.tokens_by_wordpunct if token not in stop_words and token != ''])

        # lemmatization
        self.part_of_speeches = pos_tag(self.tokens_by_wordpunct)
        for i, element in enumerate(self.part_of_speeches):
            # assuming len(self.p_o_s) == len(self.tokens_by_wp)
            token, tag = element[0], element[1]
            if not self.is_only_punctuation(token):
                self._tokens_by_wordpunct[i] = lemmatizer.lemmatize(token, self.get_wordnet_pos(tag))
                self._tokens_by_word = append(self._tokens_by_word, self._tokens_by_wordpunct[i]) 
            else:
                # corrects eventual mistakes (like tagging a '.' as a noun for example)
                self.part_of_speeches[i] = (self.part_of_speeches[i][0], "Punct")
                # note that self.p_o_s will be used when analyzing the data, that explains why it must be corrected now


    def is_only_punctuation(self, token):
        return all(char in punctuation for char in token)

    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN # By default

    @property
    def tokens_by_sentence(self):
        if self._tokens_by_sentence.size == 0:
            print("Warning: empty list of tokens by sentence. \nPlease make sure that there's data to work with.")
        return self._tokens_by_sentence

    @property
    def tokens_by_wordpunct(self):
        if self._tokens_by_wordpunct.size == 0:
            print("Warning: empty list of tokens by word/punctuation. \nPlease make sure that there's data to work with.")
        return self._tokens_by_wordpunct

    @property
    def tokens_by_word(self):
        if self._tokens_by_word.size == 0:
            print(
                "Warning: empty list of tokens by word. \nPlease make sure that there's data to work with.")
        return self._tokens_by_word

    @property
    def raw_data(self):
        if not self._raw_data:
            print("Warning: raw data is empty")
        return self._raw_data


@dataclass
class TokensStatsAndRearrangements: # To be referred as TSAR later on
    """
    MUST be used with ONE set of Tokens.
    - Provides statistical insights over ONE source (word frequency, text richness, POS...)
    """
    base: Tokenizer
    word_freq: FreqDist = field(init=False, repr=False)
    bigrams : Counter = field(init=False, repr=False)
    trigrams : Counter = field(init=False, repr=False)
    text_richness: float = field(init=False, repr=False)
    average_sentence_length: float = field(init=False, repr=False)

    def __post_init__(self):
        self.bigrams = Counter(ngrams(self.base.tokens_by_word, 2))
        self.trigrams = Counter(ngrams(self.base.tokens_by_word, 3))
        self.calculate_statistics()

    def calculate_statistics(self):
        self.word_freq = FreqDist(self.base.tokens_by_word)
        if len(self.base.tokens_by_word) == 0:
            print("Warning : cannot evaluate text richness because there are no tokens to work with.")
            self.text_richness = 0
        else:
            self.text_richness = len(set(self.base.tokens_by_word)) / \
                len(self.base.tokens_by_word)

    def display_statistics(self):
        print(f"Word Frequency (WordPunct): {self.word_freq.most_common(5)}")
        print(f"Text Richness: {self.text_richness}")


@dataclass
class TextProcessingAlgorithms: # To be referred as TPA later on
    """
    #TODO
    MUST be used with TWO sets of Tokens.
    Applies fundamental algorithms to evaluate similarity between TWO sources 
    (like cosine similarity, n-grams similarity...) and stores the results.
    """
    input_tokens_sets : TokensStatsAndRearrangements = field(init=True)
    source_tokens_sets : TokensStatsAndRearrangements = field(init=True)
    _cosine_similarity : float = field(init=False, default=-1) # -1 is a sentinel value
    _jaccard_similarity : float = field(init=False, default=-1)

    #bigrams structure : {(word1, word2) : (input_text_occurences, source_text_occurences)}
    _identical_bigrams : dict[tuple[str, str]: tuple[int, int]] = field(init=False, repr=False)
    ##trigrams structure : {(word1, word2, word3) : (input_text_occurences, source_text_occurences)}
    _identical_trigrams : dict[tuple[str, str, str]: tuple[int, int]] = field(init=False, repr=False)

    def __post_init__(self):
        self._identical_bigrams = {}
        self._identical_trigrams = {}

    @property
    def cosine_similarity(self):
        """
        This property has been written like an actual function since the cosine sim calculation will be
        done at most once anyway. Plus, it is not certain that every algorithm applied in this
        class will be useful for the analysis (since it'll depend of how complex the user desires the analysis to be), 
        so calculating the thing ONLY IF NEEDED was the point of having such a @property.

        ##########
        (NOTE : could change if cosine similarity is actually necessary for every analysis no matter what - 
        should be reevaluated when we'll start working on User Experience !)
        ##########
        """
        if self._cosine_similarity == -1: # if not evaluated yet
            both_texts_words_union = set(self.input_tokens_sets.base.tokens_by_word).union(set(self.source_tokens_sets.base.tokens_by_word))
            input_norm = sqrt(sum(x**2 for x in self.input_tokens_sets.word_freq.values()))
            source_norm = sqrt(sum(y**2 for y in self.source_tokens_sets.word_freq.values()))
            dot_product = 0
            for word in both_texts_words_union:
                if word in self.input_tokens_sets.word_freq and word in self.source_tokens_sets.word_freq:
                    dot_product += self.input_tokens_sets.word_freq[word] * self.source_tokens_sets.word_freq[word]  # Fix: mul instead of add
            self._cosine_similarity = dot_product / (input_norm * source_norm)
        return self._cosine_similarity
                    
    @property
    def jaccard_similarity(self):
        """
        Same remark than for cosine sim - will maybe get moved to its own
        dedicated function.
        """
        if self._jaccard_similarity == -1:
            input_words = set(self.input_tokens_sets.word_freq.keys())
            source_words = set(self.source_tokens_sets.word_freq.keys())
            union_length = len(input_words.union(source_words))
            intersection_length = len(input_words.intersection(source_words))
            self._jaccard_similarity = intersection_length / union_length
        return self._jaccard_similarity
    
    def find_similar_ngrams(self, input_ngrams, source_ngrams):
        similar_ngrams = {}
        for ngram in input_ngrams:
            if ngram in source_ngrams:
                input_occurrences = input_ngrams[ngram]
                source_occurrences = source_ngrams[ngram]
                similar_ngrams[ngram] = (input_occurrences, source_occurrences)
        return similar_ngrams
    
    @property
    def similar_bigrams(self):
        if self._identical_bigrams == {}:
            input_bigrams = self.input_tokens_sets.bigrams
            source_bigrams = self.source_tokens_sets.bigrams
            self._identical_bigrams = self.find_similar_ngrams(input_bigrams, source_bigrams)
        return self._identical_bigrams
    
    @property
    def similar_trigrams(self):
        if self._identical_trigrams == {}:
            input_trigrams = self.input_tokens_sets.trigrams
            source_trigrams = self.source_tokens_sets.trigrams
            self._identical_trigrams = self.find_similar_ngrams(input_trigrams, source_trigrams)
        return self._identical_trigrams
