######
# ALL EXPLAINATIONS ARE IN OUR MANIFESTO :
# https://github.com/Daniel-Dfg/PlagiarismDetectionProject/blob/main/Resources/Manifesto/A%20Manifesto%20for%20PlagiaSight.md
######

#Language processing related ↴
from nltk import FreqDist, data, pos_tag
from nltk.tokenize import wordpunct_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
#from nltk.stem import WordNetLemmatizer
from lemminflect import getLemma
from nltk.util import ngrams
import re
from string import punctuation # helps to check if a string is made of punctuation only
#Containers ↴
from collections import Counter
from numpy import array, append, ndarray
from dataclasses import dataclass, field
from collections import defaultdict
#Misc ↴
from math import sqrt
from numpy import mean, median
from os import path
import os
import chardet #detects file encoding
import pymupdf #for extracting data from pdf files
#from time import time


#Global constants ↴
VALID_FILE_EXTENSIONS = [".txt"]
REGEX_SPLIT_SENTENCES = r"(?<!\w\.\w.)(?<!\b[A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?)\s|\n"
TEXT_TOO_SHORT_LIMIT = 3 #minimal amount of sentences for the analysis to be made
SENTENCES_TOO_SHORT_LIMIT = 3 #minimal amount of words/sentence on average to be considered a "valid" text
TIME = None
CUSTOM_PUNCTUATION = set(punctuation + '•"“”')

#TODO : find the main bottleneck between extract_raw, Tokenizer and TokensStatsAndRearrangements (after first optimizations)
#TODO : learn about numba Just-In-Time compiler (and its alternatives)
#TODO : implement benchmarking for basic operations; they should be documented too, to explain why we choose this way of reading text over that way (regarding speed.)
# code readability might be hurt tho, this will have to be documented too.
# Reconsider task delegation from TSAR to Tokenizer (will need benchmarking too)
@dataclass
class Tokenizer:
    _raw_data: str #init = True (given as parameter)
    _tokens_by_sentence: ndarray = field(init=False, repr=False)
    _tokens_by_wordpunct: ndarray = field(init=False, repr=False)
    _tokens_by_word: ndarray = field(init=False, repr=False, default_factory=lambda : array([]))
    _tokens_by_syntagm: ndarray = field(init=False, repr=False, default_factory=lambda : array([]))
    _part_of_speeches_tags: ndarray = field(init=False, repr=False, default_factory=lambda : array([]))

    def __post_init__(self):
        #TIME = time()
        sentences = re.split(REGEX_SPLIT_SENTENCES, self._raw_data) #Possible subbottleneck
        self._tokens_by_sentence = array([sent.strip() for sent in sentences if sent.strip()])
        if len(self._tokens_by_sentence) < TEXT_TOO_SHORT_LIMIT:
            raise UnprocessableTextContent(f"Text is too short (under {TEXT_TOO_SHORT_LIMIT} sentences detected)")
        #TIME = time()
        tokens_by_wordpunct_first_pass = wordpunct_tokenize(self._raw_data) #will be filtered in the next lines
        #TIME = time()
        pos_tags_first_pass = self._lemmatize_and_tag_tokens(tokens_by_wordpunct_first_pass) # → list[(word, pos_tag)]
        #print("Time spent lemmatizing and tagging", time() - TIME)
        #TIME = time()
        self._tokens_by_syntagm, self._tokens_by_wordpunct = self._filter_and_group_tokens(pos_tags_first_pass)
        #print("Time spent filtering and grouping", time() - TIME)


    def _lemmatize_and_tag_tokens(self, tbwp_first_pass) -> list[tuple[str, str]]: #BOTTLENECK
        #lemmatizer = WordNetLemmatizer() #kept as a backup solution, with lemmatizer.lemmatize(token, self._get_wordnet_pos(tag))
        part_of_speech_tags = []
        time_spent_lemmatizing = 0
        pos_tagged_tbwp = pos_tag(tbwp_first_pass)
        for token, tag in pos_tagged_tbwp:
            if not self._is_only_punctuation(token):
                #TIME = time()
                lemma_tuple = getLemma(token, self.get_tag_lemminflect(tag)) #optimization compared to WordNetLemmatizer
                if lemma_tuple:
                    lemmatized_form = lemma_tuple[0]
                else:
                    lemmatized_form = token
                #time_spent_lemmatizing += time() - TIME
                part_of_speech_tags.append((lemmatized_form, tag))
            else:
                part_of_speech_tags.append((token, "Punct")) #fix mistakes made by the automatic POS tagger
        #print("Time spent lemmatizing", time_spent_lemmatizing)
        return part_of_speech_tags

    def _filter_and_group_tokens(self, part_of_speech_tags) -> tuple[ndarray, ndarray]:
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
        #Possible subbottleneck : reiterating over the filtered list (might not be necessary)
        for term, pos in part_of_speech_tags: #term = either a word or a punctuation sign
            if term in stop_words or self._is_only_punctuation(term) or term == '': #if this token is a "syntagm breaker"
                if current_syntagm != []:
                    all_syntagms.append(current_syntagm)
                    current_syntagm = []
                if self._is_only_punctuation(term):
                    filtered_tokens_by_wordpunct.append(term)
                    self._part_of_speeches_tags = append(self._part_of_speeches_tags, pos)
            else:
                current_syntagm.append(term)
                filtered_tokens_by_wordpunct.append(term)
                self._part_of_speeches_tags = append(self._part_of_speeches_tags, pos)
                self._tokens_by_word = append(self._tokens_by_word, term)
        if current_syntagm:
            all_syntagms.append(current_syntagm)
        return array(all_syntagms, dtype=object), array(filtered_tokens_by_wordpunct) #TODO : Think about the usage of dtype

    def _is_only_punctuation(self, token) -> bool:
        return all(char in CUSTOM_PUNCTUATION for char in token)

    def get_tag_lemminflect(self, tag):
        if tag.startswith('J'):
            return 'ADJ'
        elif tag.startswith('V'):
            return 'VERB'
        elif tag.startswith('R'):
            return 'ADV'
        else:
            return 'NOUN' # Default

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
        if not self._part_of_speeches_tags.size:
            raise TokenListIsEmpty("words' POS tags") #since POS tags are based on token by words
        return self._part_of_speeches_tags

    @property
    def raw_data(self):
        if not self._raw_data:
            raise UnprocessableTextContent("raw data")
        return self._raw_data



class TokensStatsAndRearrangements: # To be referred as TSAR
    def __init__(self, base):
        self._base : Tokenizer = base
        self._bigrams = Counter(ngrams(self._base.tokens_by_word, 2))
        self._trigrams = Counter(ngrams(self._base.tokens_by_word, 3))
        self._word_freq = FreqDist(self._base.tokens_by_word)
        self._pos_freq = FreqDist(self._base.part_of_speeches)
        self._text_richness = len(self._base.tokens_by_word) / len(set(self._base.tokens_by_word))
        sum_of_sent_lengths = 0
        self._sent_lengths = []
        for sent in self._base.tokens_by_sentence:
            sent_length = len(word_tokenize(sent)) #Possible subbottleneck : shouldn't we have split the sentences before to extract words from it ?
            sum_of_sent_lengths += sent_length
            self._sent_lengths.append(sent_length)
        self._average_sent_length = sum_of_sent_lengths / len(self._base.tokens_by_sentence)
        self._median_sent_length = median(self._sent_lengths)
        self._syntagms_scores = {} # {syntagm : score}
        self.evaluate_syntagms_scores()

    def evaluate_syntagms_scores(self):
        #Helper to evaluate the syntagms scores based on the RAKE algorithm.
        word_degrees = defaultdict(int)
        for s in self._base.tokens_by_syntagm:
            degree = len(s) - 1
            for word in s:
                """
                if word not in word_degrees:
                    word_degrees[word] = degree
                else:
                    word_degrees[word] += degree
                """
                word_degrees[word] += degree
        words_scores = {word: word_degrees[word] / self._word_freq[word] for word in self._word_freq}

        for s in self._base.tokens_by_syntagm:
            phrase_score = sum(words_scores.get(word, 0) for word in s)
            self._syntagms_scores[' '.join(s)] = phrase_score

    @property
    def base(self):
        return self._base

    @property
    def bigrams(self):
        if not self._bigrams:
            raise UnprocessableTextContent("bigrams (no bigrams found)")
        return self._bigrams

    @property
    def trigrams(self):
        if not self._trigrams:
            raise UnprocessableTextContent("trigrams (no trigrams found)")
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
        if self._average_sent_length < SENTENCES_TOO_SHORT_LIMIT:
            raise UnprocessableTextContent("average sentence length")
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
    _input_tokens_sets : TokensStatsAndRearrangements
    _source_tokens_sets : TokensStatsAndRearrangements
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
    def input_tokens_sets(self):
        return self._input_tokens_sets

    @property
    def source_tokens_sets(self):
        return self._source_tokens_sets

    @property
    def all_term_frequencies(self):
        if not self._all_term_frequencies:
            all_terms = set(self._input_tokens_sets._word_freq.keys()).union(set(self._source_tokens_sets._word_freq.keys()))
            self._all_term_frequencies = {term : self._input_tokens_sets._word_freq.get(term, 0) + self._source_tokens_sets._word_freq.get(term, 0) for term in all_terms}
        return self._all_term_frequencies

    @property
    def cosine_sim_words(self):
        return self.cosine_similarity_computation(self._source_tokens_sets._word_freq, self._input_tokens_sets._word_freq) if self._cosine_sim_words == -1 \
        else self._cosine_sim_words

    @property
    def jaccard_sim_words(self):
        return self.jaccard_similarity_computation(set(self._source_tokens_sets._word_freq.keys()), set(self._input_tokens_sets._word_freq.keys())) if self._jaccard_sim_words == -1 \
        else self._jaccard_sim_words

    @property
    def cosine_sim_pos(self):
        return self.cosine_similarity_computation(self._source_tokens_sets._pos_freq, self._input_tokens_sets._pos_freq) if self._cosine_sim_pos == -1 \
        else self._cosine_sim_pos

    @property
    def jaccard_sim_pos(self):
        return self.jaccard_similarity_computation(set(self._source_tokens_sets._pos_freq.keys()), set(self._input_tokens_sets._pos_freq.keys())) if self._jaccard_sim_pos == -1 \
        else self._jaccard_sim_pos

    def find_similar_ngrams(self, input_ngrams, source_ngrams):
        similar_ngrams = {}
        for ngram in input_ngrams:
            if ngram in source_ngrams: #Possible subbottleneck : subloop each time, unefficient. Might be better to :
                # a) hash then lookup
                # b) less memory-consuming approach ?
                input_occurrences = input_ngrams[ngram]
                source_occurrences = source_ngrams[ngram]
                similar_ngrams[ngram] = (input_occurrences, source_occurrences)
        return similar_ngrams

    @property
    def similar_bigrams(self):
        if self._identical_bigrams == {}:
            input_bigrams = self._input_tokens_sets._bigrams
            source_bigrams = self._source_tokens_sets._bigrams
            self._identical_bigrams = self.find_similar_ngrams(input_bigrams, source_bigrams)
        return self._identical_bigrams

    @property
    def similar_trigrams(self):
        if self._identical_trigrams == {}:
            input_trigrams = self._input_tokens_sets._trigrams
            source_trigrams = self._source_tokens_sets._trigrams
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

#Custom exceptions
class TokenListIsEmpty(Exception):
    def __init__(self, tokens_by):
        self.message = "Warning: empty list of " + tokens_by + ": \nPlease make sure that there's data to work with."
        super().__init__(self.message)

class UnprocessableTextContent(Exception):
    def __init__(self, attribute) -> None:
        self.message = "Warning: the text can't be processed properly because : "
        possible_errors = {
            "tokens by syntagm": "tokens by syntagm list is empty, showing that the text is either not in English or only made of stop words/punctuation.",
            "raw data": "raw data (e.g the text extracted from a certain source file, whether it is the user's or something scraped from the web) is empty.",
            "text richness": "Warning: text richness is 1, meaning that the text is either not in English or made of words all different to one another (so it's probably too short to be analyzed).",
            "average sentence length" : f"sentences are too short on average to be considered as valid sentences. Bottom limit is {SENTENCES_TOO_SHORT_LIMIT} words/sentence."
            }
        self.message += possible_errors.get(attribute, attribute)
        super().__init__(self.message)


def extract_raw_from_file(file_path: str, file_format: str) -> str:
    if not path.exists(file_path):
        raise FileNotFoundError(f"{file_path} doesn't exist")
    if file_format not in ("txt", "pdf"):
        raise ValueError(f"Invalid file format: {file_format}")

    if file_format == "pdf":
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = convert_pdf_to_txt(file_path, temp_dir)
    with open(file_path, 'rb') as file:  # Detects the encoding of file
        raw_data = file.read()
        result = chardet.detect(raw_data)
        file_encoding = result['encoding']
    with open(file_path, 'r', encoding=file_encoding, errors='ignore') as f:
        return f.read().lower()


def convert_pdf_to_txt(file_path: str, temp_dir_path: str) -> str:
    """
    Returns the path of the pdf file converted to a txt file.
    """
    pdf_file = pymupdf.open(file_path)
    converted_file_path = os.path.join(temp_dir_path, os.path.basename(file_path).replace(".pdf", ".txt"))
    with open(converted_file_path, "wb") as out:
        for page in pdf_file:
            out.write(page.get_text().encode("utf-8"))
    return converted_file_path
"""
#FOR TESTING PURPOSES (feel free to uncomment and play around with this)
def test_sentences_tokenized():
    poem_content = extract_raw_from_file("Resources/Sample Data/BasicTexts/" + "poem1.txt")
    poem_tokens = Tokenizer(poem_content)

    sentence_tokens_poem = [str(token) for token in list(
        poem_tokens.tokens_by_sentence)]
    print(sentence_tokens_poem)
test_sentences_tokenized()
"""
