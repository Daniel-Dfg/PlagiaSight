"""
Note from Onur:
I needed to convert each token, words, etc to str since they were
np.str type and I needed to compare strings (from numpy).
"""

import pytest
import unittest
import nltk
import chardet
from src import Tokenizer, TokensStatsAndRearrangements, TokensComparisonAlgorithms
from random import choice
from os import path


testfiles_path_basic = "Resources/Sample Data/BasicTexts/"
testfiles_path_complex = "Resources/Sample Data/ComplexTexts/"  # TODO


class TestTextAnalysis(unittest.TestCase):
    def setUp(self):
        # Need these for the tests to work
        nltk.download('averaged_perceptron_tagger_eng')
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')

        self.poem_file_path = testfiles_path_basic + "poem1.txt"
        self.source_file_path = testfiles_path_basic + "source.txt"

        def extract_raw_from_file(file_path: str) -> str:
            if not path.exists(file_path):
                raise FileNotFoundError("Specified file doesn't exist")

            with open(file_path, 'rb') as file:  # Detects the encoding of file
                raw_data = file.read()
                result = chardet.detect(raw_data)
                file_encoding = result['encoding']

            with open(file_path, 'r', encoding=file_encoding, errors='ignore') as f:
                return f.read().lower()

        poem_content = extract_raw_from_file(self.poem_file_path)
        source_content = extract_raw_from_file(self.source_file_path)

        self.poem_tokens = Tokenizer(poem_content)
        self.source_tokens = Tokenizer(source_content)

        self.poem_TSAR = TokensStatsAndRearrangements(self.poem_tokens)
        self.source_TSAR = TokensStatsAndRearrangements(
            self.source_tokens)

        self.tpa = TokensComparisonAlgorithms(
            input_tokens_sets=self.poem_TSAR, source_tokens_sets=self.source_TSAR)

    def test_word_tokenization(self):
        expected_tokens = [
            'march', 'abyss', 'look', 'acknowledge',
            'existence', 'live', 'life', 'full'
        ]
        word_tokens_poem = [str(token)
                            for token in list(self.poem_tokens.tokens_by_word)]
        self.assertListEqual(word_tokens_poem, expected_tokens)

    def test_wordpunct_tokenization(self):
        expected_tokens = [
            'march', 'abyss', '.', 'look', ',', 'acknowledge',
            'existence', '.', 'live', 'life', 'full', '.'
        ]
        wordpunct_tokens_poem = [str(token) for token in list(
            self.poem_tokens.tokens_by_wordpunct)]
        self.assertListEqual(wordpunct_tokens_poem, expected_tokens)

    def test_sentence_tokenization(self):
        expected_sentences = [
            'march into the abyss', 'look down,',
            'acknowledge your existence', 'live your life at fullest'
        ]
        sentence_tokens_poem = [str(token) for token in list(
            self.poem_tokens.tokens_by_sentence)]
        self.assertListEqual(sentence_tokens_poem, expected_sentences)

    def test_syntagm_tokenization(self):
        expected_syntagms = [
            ['march'], ['abyss'], ['look'], ['acknowledge'],
            ['existence'], ['live'], ['life'], ['full']
        ]
        syntagm_tokens_poem = [[str(token)for token in syntagm]
                               for syntagm in self.poem_tokens.tokens_by_syntagm]
        self.assertEqual(len(syntagm_tokens_poem), len(expected_syntagms))
        for syntagm, expected in zip(syntagm_tokens_poem, expected_syntagms):
            self.assertListEqual(syntagm, expected)

    def test_syntagms_scores(self):
        self.poem_TSAR.evaluate_syntagms_scores()  # Calculate keywords_score
        expected_keywords_score = {
            'march': 0.0, 'abyss': 0.0, 'look': 0.0, 'acknowledge': 0.0,
            'existence': 0.0, 'live': 0.0, 'life': 0.0, 'full': 0.0
        }
        self.assertEqual(len(self.poem_TSAR.syntagms_scores),
                         len(expected_keywords_score))
        self.assertDictEqual(self.poem_TSAR.syntagms_scores,
                             expected_keywords_score)

    def test_all_term_freq(self):
        expected_all_term_freq = {
            'march': 2, 'abyss': 1, 'light': 1, 'look': 2, 'acknowledge': 2,
            'existence': 2, 'live': 2, 'life': 2, 'full': 2
        }
        self.assertEqual(len(expected_all_term_freq),
                         len(self.tpa.all_term_frequencies))
        self.assertDictEqual(self.tpa.all_term_frequencies,
                             expected_all_term_freq)

    def test_cosine_sim_words_and_pos(self):
        self.assertEqual(round(self.tpa.cosine_sim_words, 3), 0.875)
        self.assertEqual(self.tpa.cosine_sim_pos, 1.0)

    def test_jaccard_sim_words_and_pos(self):
        self.assertEqual(round(self.tpa.jaccard_sim_words, 3), 0.778)
        self.assertEqual(self.tpa.jaccard_sim_pos, 1.0)

    def test_similar_bigrams(self):
        expected_similar_bigrams = {
            ('look', 'acknowledge'): (1, 1), ('acknowledge', 'existence'): (1, 1),
            ('existence', 'live'): (1, 1), ('live', 'life'): (1, 1), ('life', 'full'): (1, 1)
        }
        o_similar_bigrams = {tuple(
            str(gram) for gram in key): value for key, value in self.tpa.similar_bigrams.items()}
        self.assertDictEqual(o_similar_bigrams, expected_similar_bigrams)

    def test_similar_trigrams(self):
        expected_similar_trigrams = {
            ('look', 'acknowledge', 'existence'): (1, 1), ('acknowledge', 'existence', 'live'): (1, 1),
            ('existence', 'live', 'life'): (1, 1), ('live', 'life', 'full'): (1, 1)
        }
        o_similar_trigrams = {tuple(
            str(gram) for gram in key): value for key, value in self.tpa.similar_trigrams.items()}
        self.assertDictEqual(o_similar_trigrams, expected_similar_trigrams)

    # Sould I do a test_similar_ngrams(self)?
    """
    def test_random_assigment(self):
        ... #TODO (but not really a priority right now)
    """


if __name__ == '__main__':
    unittest.main()
