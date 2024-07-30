#TODO : support different file types (like .pdf, .md, etc.)

from string import punctuation # helps to check if a string is made of punctuation only here
from math import sqrt
from numpy import array, append, flexible
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist, pos_tag
from dataclasses import dataclass, field
from os import path
from collections import Counter
from nltk.util import ngrams
import nltk


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
    _tokens_by_word: array = field(init=False, repr=False, default_factory=lambda: array([])) # will be created after tokens by wordpunct curation
    _tokens_by_syntagm: array = field(init=False, repr=False, default_factory=lambda :array([])) # will be created later (must clear that #TODO)
    _part_of_speeches: array = field(init=False, repr=False, default_factory=lambda:array([])) #only contains the pos tags themselves, not the words/punct signs
    #_top_common_word_sentences: array = field(init=False, repr=False)

    def __post_init__(self):
        #MUST RENAME FUCTIONS PROPERLY #TODO
        self.extract_raw_from_file()
        self.tokenize_text()
        self.clean_data()

    def extract_raw_from_file(self):
        if not path.exists(self.file):
            raise FileNotFoundError("Specified file doesn't exist")
        with open(self.file, 'r', encoding='utf-8-sig', errors='ignore') as f: #might consider chardet or cchardet to detect encoding
            self._raw_data = f.read().lower()

    def tokenize_text(self):
        tokens_by_sentence_first_pass = array(self.raw_data.replace('\n', 'þ').replace('.', 'þ').split('þ'))
        self._tokens_by_sentence = array([sent.strip() for sent in tokens_by_sentence_first_pass if sent.strip()])
        self._tokens_by_wordpunct = array(wordpunct_tokenize(self.raw_data))

    def clean_data(self):
        # Needs doc and clarification #TODO
        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        pos_first_pass = pos_tag(self.tokens_by_wordpunct)
        for i, element in enumerate(pos_first_pass):
            token, tag = element[0], element[1]
            if not self.is_only_punctuation(token):
                self._tokens_by_wordpunct[i] = lemmatizer.lemmatize(token, self.get_wordnet_pos(tag))
            else:
                tag = "Punct"
                pos_first_pass[i] = (pos_first_pass[i][0], "Punct")
        stop_words = set(stopwords.words('english'))
        i = 0
        new_tokens_by_wordpunct = array([])
        syntagms = []  # Temporary list to hold syntagms
        current_syntagm = []

        for i, word in enumerate(self.tokens_by_wordpunct): # len(tok_by_wp) == len(pos_first_pass) at this point : time for filtering
            if word in stop_words or self.is_only_punctuation(word) or word == '':
                if current_syntagm != []:
                    syntagms.append(current_syntagm)
                    current_syntagm = []
                if self.is_only_punctuation(word):
                    new_tokens_by_wordpunct = append(new_tokens_by_wordpunct, word)
                    self._part_of_speeches = append(self._part_of_speeches, pos_first_pass[i][1])
            else:
                current_syntagm.append(word)
                new_tokens_by_wordpunct = append(new_tokens_by_wordpunct, word)
                self._part_of_speeches = append(self._part_of_speeches, pos_first_pass[i][1])
                self._tokens_by_word = append(self._tokens_by_word, word)
            i += 1

        if current_syntagm:
            syntagms.append(current_syntagm)

        self._tokens_by_syntagm = array(syntagms, dtype=object) #not clean at all conversion, might fix later
        self._tokens_by_wordpunct = new_tokens_by_wordpunct
        #filtering done

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
    def tokens_by_syntagm(self):
        if self._tokens_by_syntagm.size == 0:
            print("Warning: empty list of tokens by syntagm. \nPlease make sure that there's data to work with.")
        return self._tokens_by_syntagm
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
            print("Warning: empty list of tokens by word. \nPlease make sure that there's data to work with.")
        return self._tokens_by_word

    @property
    def part_of_speeches(self):
        if self._part_of_speeches.size == 0:
            print("Warning")
        return self._part_of_speeches

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
        as well as rearrangements for comparison between texts (via bigrams and trigrams)
        and key phrases (to make web scraping possible afterwards)

    Extracting keyphrases from like, a web page would be still useful, as comparing keyphrases from
    the input and the source would allow us to conjecture (with a certain uncertainty still) if they go over the same subjects.
    This idea would help us distinguish STRUCTURAL similarities in the text from WORD similarities (since one doesn't imply the other).
    """
    base: Tokenizer
    word_freq: FreqDist = field(init=False, repr=False)
    pos_freq:FreqDist = field(init=False, repr=False)
    bigrams : Counter = field(init=False, repr=False)
    trigrams : Counter = field(init=False, repr=False)
    text_richness: float = field(init=False, repr=False)
    average_sentence_length: float = field(init=False, repr=False)
    keywords_scores: dict = field(init=False, repr=False)

    def __post_init__(self):
        self.keywords_scores = {}
        self.bigrams = Counter(ngrams(self.base.tokens_by_word, 2))
        self.trigrams = Counter(ngrams(self.base.tokens_by_word, 3))
        self.word_freq = FreqDist(self.base.tokens_by_word)
        self.pos_freq = FreqDist(self.base.part_of_speeches)
        self.text_richness = len(self.base.tokens_by_word) / len(set(self.base.tokens_by_word))
        self.average_sentence_length = sum(len(sent.split()) for sent in self.base.tokens_by_sentence) / len(self.base.tokens_by_sentence)
        self.get_syntagms_scores()
        #self.display_statistics()

    def display_statistics(self):
        print(f"Word Frequency (WordPunct): {self.word_freq.most_common(5)}")
        print(f"Text Richness: {self.text_richness}")
        print(f"Average Sentence Length: {self.average_sentence_length}")
        print(f"Bigrams: {self.bigrams.most_common(5)}")
        print(f"Trigrams: {self.trigrams.most_common(5)}")

    def get_syntagms_scores(self):
        word_degrees = {}
        for s in self.base.tokens_by_syntagm:
            degree = len(s) - 1
            for word in s:
                if word not in word_degrees:
                    word_degrees[word] = 0
                else:
                    word_degrees[word] += degree
        words_scores = {word: word_degrees[word] / self.word_freq[word] for word in self.word_freq}
        for s in self.base.tokens_by_syntagm:
            phrase_score = sum(words_scores[word] for word in s)
            self.keywords_scores[' '.join(s)] = phrase_score


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
    _cosine_sim_words : float = field(init=False, default=-1) # -1 is a sentinel value
    _jaccard_sim_words : float = field(init=False, default=-1)
    _cosine_sim_pos : float = field(init=False, default=-1)
    _jaccard_sim_pos : float = field(init=False, default=-1)

    #bigrams structure : {(word1, word2) : (input_text_occurences, source_text_occurences)}
    _identical_bigrams : dict[tuple[str, str]: tuple[int, int]] = field(init=False, repr=False, default_factory=dict)
    ##trigrams structure : {(word1, word2, word3) : (input_text_occurences, source_text_occurences)}
    _identical_trigrams : dict[tuple[str, str, str]: tuple[int, int]] = field(init=False, repr=False, default_factory=dict)

    def __post_init__(self):
        """
            #will do a function launch_analysis #TODO
            print(f"Cosine Similarity: {self.cosine_similarity}")
            print(f"Jaccard Similarity: {self.jaccard_similarity}")
            print("Similar Bigrams:")
            for bigram, occurrences in self.similar_bigrams.items():
                print(f"{bigram}: {occurrences}")
            print("Similar Trigrams:")
            for trigram, occurrences in self.similar_trigrams.items():
                print(f"{trigram}: {occurrences}")
        """
    def cosine_similarity(self, source_terms : dict, input_terms : dict) -> float: #both args are WordFreqs (from pos or words)
        both_texts_words_union = set(source_terms.keys()).union(set(input_terms.keys()))
        input_norm = sqrt(sum(x**2 for x in input_terms.values()))
        source_norm = sqrt(sum(y**2 for y in source_terms.values()))
        dot_product = 0
        for word in both_texts_words_union:
            if word in source_terms.keys() and word in input_terms.keys():
                dot_product += source_terms[word] * input_terms[word]
        return dot_product / (input_norm * source_norm)

    def jaccard_similarity(self, source_terms : set, input_terms : set) -> float:
        intersection_size = len(input_terms.intersection(source_terms))
        union_size = len(input_terms.union(source_terms))
        return intersection_size / union_size

    @property
    def cosine_sim_words(self):
        return self.cosine_similarity(self.source_tokens_sets.word_freq, self.input_tokens_sets.word_freq) if self._cosine_sim_words == -1 else self._cosine_sim_words

    @property
    def jaccard_sim_words(self):
        return self.jaccard_similarity(set(self.source_tokens_sets.word_freq.keys()), set(self.input_tokens_sets.word_freq.keys())) if self._jaccard_sim_words == -1 else self._jaccard_sim_words

    @property
    def cosine_sim_pos(self):
        return self.cosine_similarity(self.source_tokens_sets.pos_freq, self.input_tokens_sets.pos_freq) if self._cosine_sim_pos == -1 else self._cosine_sim_pos

    @property
    def jaccard_sim_pos(self):
        return self.jaccard_similarity(set(self.source_tokens_sets.pos_freq.keys()), set(self.input_tokens_sets.pos_freq.keys())) if self._jaccard_sim_pos == -1 else self._jaccard_sim_pos

    def jaccard_sim(self):
        """
        Same remark than for cosine sim - will maybe get moved to its own
        dedicated function.
        """
        if self._jaccard_sim_words == -1:
            input_words = set(self.input_tokens_sets.word_freq.keys())
            source_words = set(self.source_tokens_sets.word_freq.keys())
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


#t = "/home/daniel/Documents/INFO/PersonalProjects/PlagiarismDetectionProject/Resources/Sample Data/BasicTexts/DataFromText-MiningProject/ass1-202.txt"
t2 = "./Resources/Sample Data/BasicTexts/poem1.txt"
#t2 = "../Resources/Sample Data/BasicTexts/DataFromText-MiningProject/ass1-211.txt"
tok = Tokenizer(file=t2)
#tsar = TokensStatsAndRearrangements(base=tok)
#tok2 = Tokenizer(file=t2)
#tsar2 = TokensStatsAndRearrangements(base=tok2)

#tpa = TextProcessingAlgorithms(input_tokens_sets=tsar, source_tokens_sets=tsar2)

print('SENTENCE')
print(tok.tokens_by_sentence)
print('-----------')
print('WORDPUNCT')
print(tok.tokens_by_wordpunct)
print('-----------')
print('POS')
print(tok.part_of_speeches)
print('-------------')
print('WORD')
print(tok.tokens_by_word)
print('-----------')
print('SYNTAGM')
for tt in tok.tokens_by_syntagm:
    print(tt)
#print(tok.raw_data)"""
