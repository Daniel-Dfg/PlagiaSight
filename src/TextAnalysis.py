######
#ALL EXPLAINATIONS ARE IN OUR MANIFESTO :
# https://github.com/LUCKYINS/PlagiarismDetectionProject
######

#Language processing related ↴
from nltk import FreqDist, data, pos_tag
from nltk.tokenize import simple, wordpunct_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import re
from string import punctuation # helps to check if a string is made of punctuation only
#Containers ↴
from collections import Counter
from numpy import array, append, flexible, ndarray
from dataclasses import dataclass, field
#Misc ↴
from math import sqrt
from numpy import mean, median
from os import path
import chardet


@dataclass
class Tokenizer:
    _raw_data: str #init = True (given as parameter)
    _tokens_by_sentence: ndarray = field(init=False, repr=False)
    _tokens_by_wordpunct: ndarray = field(init=False, repr=False)
    _tokens_by_word: ndarray = field(init=False, repr=False, default_factory=lambda: array([]))
    _tokens_by_syntagm: ndarray = field(init=False, repr=False, default_factory=lambda: array([])) #syntagm = sequence of contiguous words that are not stopwords, punctuation or empty strings
    _part_of_speeches: ndarray = field(init=False, repr=False, default_factory=lambda: array([]))

    def __post_init__(self):
        sentences = re.split(r"(?<!\w\.\w.)(?<!\b[A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?)\s|\n", self._raw_data)
        self._tokens_by_sentence = array([sent.strip() for sent in sentences if sent.strip()])
        tokens_by_wordpunct_first_pass = array(wordpunct_tokenize(self._raw_data)) #first pass, will be filtered in the next lines
        pos_tags_first_pass = self._lemmatize_and_tag_tokens(tokens_by_wordpunct_first_pass) # → list[(word, pos_tag)]
        self._tokens_by_syntagm, self._tokens_by_wordpunct = self._filter_and_group_tokens(pos_tags_first_pass)


    def _lemmatize_and_tag_tokens(self, tbwp_first_pass) -> list[tuple[str, str]]:
        lemmatizer = WordNetLemmatizer()
        pos_tags = []
        for token, tag in pos_tag(tbwp_first_pass):
            if not self._is_only_punctuation(token):
                lemmatized_token = lemmatizer.lemmatize(token, self._get_wordnet_pos(tag))
                pos_tags.append((lemmatized_token, tag))
            else:
                pos_tags.append((token, "Punct"))
        return pos_tags

    def _filter_and_group_tokens(self, pos_tags) -> tuple[ndarray, ndarray]:
        """
        3 responsibilities:
        1) Filtering : remove stopwords, punctuation, empty strings
        2) Building the tokens by word with the filtered tokens (those that have been lemmatized and POS tagged earlier)
        3) Grouping : group tokens by syntagm

        These 3 responsibilities were grouped to be done in one only loop, at the cost of readability.
        """
        stop_words = set(stopwords.words('english')) #might consider adding more languages in the future
        filtered_tokens_by_wordpunct = []
        all_syntagms = []
        current_syntagm = []
        for term, pos in pos_tags: #term = either a word or a punctuation sign
            if term in stop_words or self._is_only_punctuation(term) or term == '': #if this token is a "syntagm breaker"
                if current_syntagm != []:
                    all_syntagms.append(current_syntagm)
                    current_syntagm = []
                if self._is_only_punctuation(term):
                    filtered_tokens_by_wordpunct.append(term)
                    self._part_of_speeches = append(self._part_of_speeches, pos)
            else:
                current_syntagm.append(term)
                filtered_tokens_by_wordpunct.append(term)
                self._part_of_speeches = append(self._part_of_speeches, pos)
                self._tokens_by_word = append(self._tokens_by_word, term)
        if current_syntagm:
            all_syntagms.append(current_syntagm)
        return array(all_syntagms, dtype=object), array(filtered_tokens_by_wordpunct) #TODO : Think about the usage of dtype


    def _is_only_punctuation(self, token) -> bool:
        return all(char in punctuation for char in token)

    def _get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN  # Default

    @property
    def tokens_by_sentence(self):
        if not self._tokens_by_sentence.size:
            raise TokenListIsEmpty("tokens by sentence")
        return self._tokens_by_sentence

    @property
    def tokens_by_wordpunct(self):
        if not self._tokens_by_wordpunct.size:
            raise TokenListIsEmpty("tokens by word/punctuation")
        return self._tokens_by_wordpunct

    @property
    def tokens_by_word(self):
        if not self._tokens_by_word.size:
            raise TokenListIsEmpty("tokens by word")
        return self._tokens_by_word

    @property
    def tokens_by_syntagm(self):
        if not self._tokens_by_syntagm.size:
            raise UnprocessableTextContent("tokens by syntagm")
        return self._tokens_by_syntagm

    @property
    def part_of_speeches(self):
        if not self._part_of_speeches.size:
            raise TokenListIsEmpty("words' POS tags") #since POS tags are based on token by words
        return self._part_of_speeches

    @property
    def raw_data(self):
        if not self._raw_data:
            raise UnprocessableTextContent("raw data")
            print("Warning: raw data is empty")
        return self._raw_data


#Custom exceptions (used in Tokenizer only)
class TokenListIsEmpty(Exception):
    def __init__(self, tokens_by):
        self.message = "Warning: empty list of " + tokens_by + ". \nPlease make sure that there's data to work with."
        super().__init__(self.message)

class UnprocessableTextContent(Exception):
    def __init__(self, attribute) -> None:
        self.message = "Warning: the text can't be processed properly because : "
        if attribute == "tokens by syntagm":
            self.message += "tokens by syntagm list is empty, showing that the text is either not in English or only made of stop words/punctuation."
        elif attribute == "raw data":
            self.message += "raw data (e.g the text extracted from a certain source file, wether it is the user's or something scraped from the web) is empty."
        elif attribute == "text richness":
            self.message += "Warning: text richness is 1, meaning that the text is either not in English or made of words all different to one another (so it's probably too short to be analyzed)."

        super().__init__(self.message)


class TokensStatsAndRearrangements: # To be referred as TSAR
    def __init__(self, base):
        self.base : Tokenizer = base
        self._bigrams = Counter(ngrams(self.base.tokens_by_word, 2))
        self._trigrams = Counter(ngrams(self.base.tokens_by_word, 3))
        self._word_freq = FreqDist(self.base.tokens_by_word)
        self._pos_freq = FreqDist(self.base.part_of_speeches)
        self._text_richness = len(self.base.tokens_by_word) / len(set(self.base.tokens_by_word))
        sum_of_sent_lengths = 0
        self._sent_lengths = []
        for sent in self.base.tokens_by_sentence:
            sent_length = len(sent.split())
            sum_of_sent_lengths += sent_length  #TODO : get more accurate measurements (e.g consider punctuation to split words using RegExes)
            self._sent_lengths.append(sent_length)
        self._average_sent_length = sum_of_sent_lengths / len(self.base.tokens_by_sentence)
        self._median_sent_length = median(self._sent_lengths)
        self._syntagms_scores = {} #syntagm : score
        self.evaluate_syntagms_scores()

    def evaluate_syntagms_scores(self):
        #Helper to evaluate the syntagms scores based on the RAKE algorithm.
        word_degrees = {}
        for s in self.base.tokens_by_syntagm:
            degree = len(s) - 1
            for word in s:
                if word not in word_degrees:
                    word_degrees[word] = degree
                else:
                    word_degrees[word] += degree
        words_scores = {word: word_degrees[word] / self._word_freq[word] for word in self._word_freq}
        for s in self.base.tokens_by_syntagm:
            phrase_score = sum(words_scores[word] for word in s)
            self._syntagms_scores[' '.join(s)] = phrase_score

    #TODO : refine the usage off these properties when needed.
    @property
    def bigrams(self):
        return self._bigrams

    @property
    def trigrams(self):
        return self._trigrams

    @property
    def word_freq(self):
        return self._word_freq

    @property
    def pos_freq(self):
        return self._pos_freq

    @property
    def text_richness(self):
        if self._text_richness == 1:
            raise UnprocessableTextContent("text richness")
        return self._text_richness

    @property
    def sent_lengths(self):
        return self._sent_lengths

    @property
    def average_sent_length(self):
        return self._average_sent_length

    @property
    def median_sent_length(self):
        return self._median_sent_length

    @property
    def syntagms_scores(self):
        return self._syntagms_scores


@dataclass
class TokensComparisonAlgorithms: # To be referred as TCA
    #Works as a "on-demand" class (meaning that the results are computed only when needed) for modularity purposes.
    input_tokens_sets : TokensStatsAndRearrangements
    source_tokens_sets : TokensStatsAndRearrangements
    _cosine_sim_words : float = field(init=False, default=-1) # -1 is a sentinel value
    _jaccard_sim_words : float = field(init=False, default=-1)
    _cosine_sim_pos : float = field(init=False, default=-1)
    _jaccard_sim_pos : float = field(init=False, default=-1)
    _all_term_frequencies : dict[str, float] = field(init=False, default_factory=dict)

    #bigrams structure : {(word1, word2) : (amount_of_input_text_occurences, amount_of_source_text_occurences)}
    _identical_bigrams : dict[tuple[str, str], tuple[int, int]] = field(init=False, repr=False, default_factory=dict)
    ##trigrams structure : {(word1, word2, word3) : (amount_of_input_text_occurences, amount_of_source_text_occurences)}
    _identical_trigrams : dict[tuple[str, str, str], tuple[int, int]] = field(init=False, repr=False, default_factory=dict)

    def __post_init__(self):
        pass

    @property
    def all_term_frequencies(self):
        if not self._all_term_frequencies:
            all_terms = set(self.input_tokens_sets._word_freq.keys()).union(set(self.source_tokens_sets._word_freq.keys()))
            self._all_term_frequencies = {term : self.input_tokens_sets._word_freq.get(term, 0) + self.source_tokens_sets._word_freq.get(term, 0) for term in all_terms}
        return self._all_term_frequencies

    def cosine_similarity_computation(self, source_terms : FreqDist, input_terms : FreqDist) -> float: #both args are WordFreqs (from pos or words)
        both_texts_words_union = set(source_terms.keys()).union(set(input_terms.keys()))
        input_norm = sqrt(sum(x**2 for x in input_terms.values()))
        source_norm = sqrt(sum(y**2 for y in source_terms.values()))
        dot_product = 0
        for word in both_texts_words_union:
            if word in source_terms.keys() and word in input_terms.keys():
                dot_product += source_terms[word] * input_terms[word]
        return dot_product / (input_norm * source_norm)

    def jaccard_similarity_computation(self, source_terms : set, input_terms : set) -> float:
        intersection_size = len(input_terms.intersection(source_terms))
        union_size = len(input_terms.union(source_terms))
        return intersection_size / union_size

    @property
    def cosine_sim_words(self):
        return self.cosine_similarity_computation(self.source_tokens_sets._word_freq, self.input_tokens_sets._word_freq) if self._cosine_sim_words == -1 \
        else self._cosine_sim_words

    @property
    def jaccard_sim_words(self):
        return self.jaccard_similarity_computation(set(self.source_tokens_sets._word_freq.keys()), set(self.input_tokens_sets._word_freq.keys())) if self._jaccard_sim_words == -1 \
        else self._jaccard_sim_words

    @property
    def cosine_sim_pos(self):
        return self.cosine_similarity_computation(self.source_tokens_sets._pos_freq, self.input_tokens_sets._pos_freq) if self._cosine_sim_pos == -1 \
        else self._cosine_sim_pos

    @property
    def jaccard_sim_pos(self):
        return self.jaccard_similarity_computation(set(self.source_tokens_sets._pos_freq.keys()), set(self.input_tokens_sets._pos_freq.keys())) if self._jaccard_sim_pos == -1 \
        else self._jaccard_sim_pos

    def jaccard_sim(self):
        if self._jaccard_sim_words == -1:
            input_words = set(self.input_tokens_sets._word_freq.keys())
            source_words = set(self.source_tokens_sets._word_freq.keys())
            union_length = len(input_words.union(source_words))
            intersection_length = len(input_words.intersection(source_words))
            self._jaccard_sim_words = intersection_length / union_length
        return self._jaccard_sim_words

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
            input_bigrams = self.input_tokens_sets._bigrams
            source_bigrams = self.source_tokens_sets._bigrams
            self._identical_bigrams = self.find_similar_ngrams(input_bigrams, source_bigrams)
        return self._identical_bigrams

    @property
    def similar_trigrams(self):
        if self._identical_trigrams == {}:
            input_trigrams = self.input_tokens_sets._trigrams
            source_trigrams = self.source_tokens_sets._trigrams
            self._identical_trigrams = self.find_similar_ngrams(input_trigrams, source_trigrams)
        return self._identical_trigrams

    """
    #FOR TESTING PURPOSES (feel free to uncomment and play around with this)
    def display_simple_results(self):
        print(f"Simple results:")
        print(f"Text1 richness: {self.source_tokens_sets.text_richness}, Text2 richness: {self.input_tokens_sets.text_richness}")
        print(f"Words cosine similarity: {self.cosine_sim_words}")
        print(f"Words Jaccard similarity: {self.jaccard_sim_words}")
        print(f"average sentence length: {self.source_tokens_sets.average_sent_length}, {self.input_tokens_sets.average_sent_length}")

    def display_complex_results(self):
        print(f"Complex results:")
        self.display_simple_results()
        print(f"POS cosine similarity: {self.cosine_sim_pos}")
        print(f"POS Jaccard similarity: {self.jaccard_sim_pos}")
        print(f"Similar bigrams: {self.similar_bigrams}")
        print(f"Similar trigrams: {self.similar_trigrams}")
    """


def extract_raw_from_file(file_path: str) -> str:
    if not path.exists(file_path):
        raise FileNotFoundError(f"{file_path} doesn't exist")

    with open(file_path, 'rb') as file:  # Detects the encoding of file
        raw_data = file.read()
        result = chardet.detect(raw_data)
        file_encoding = result['encoding']

    with open(file_path, 'r', encoding=file_encoding, errors='ignore') as f:
        return f.read().lower()
