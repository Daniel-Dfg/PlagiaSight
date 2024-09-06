import pytest
import unittest
import nltk
import chardet
from src import Tokenizer, TokensStatsAndRearrangements, TextProcessingAlgorithms
from random import choice


testfiles_path_basic = "Resources/Sample Data/BasicTexts/"
testfiles_path_complex = "Resources/Sample Data/ComplexTexts/"
class Test1(unittest.TestCase):
    def setUp(self):
        nltk.download('averaged_perceptron_tagger_eng')
        nltk.download('punkt')  # Add any other necessary resources here
        nltk.download('wordnet')
        nltk.download('stopwords')

        self.poem_file = testfiles_path_basic + "poem1.txt"
        random_assignment_suffix = ["202.txt", "211.txt", "321.txt"]
        self.random_assignment = testfiles_path_basic \
            + "DataFromText-MiningProject/ass1-" \
            + f"{choice(random_assignment_suffix)}"
        
        # Detects the encoding of the file
        with open(self.poem_file, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding_poem = result['encoding']

        with open(self.random_assignment, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding_assignment = result['encoding']

        # Open the file with detected encoding
        with open(self.poem_file, 'r', encoding=encoding_poem) as file:
            poem_content = file.read()
        with open(self.random_assignment, 'r', encoding=encoding_assignment) as file:
            random_assignment_content = file.read()

        self.poem_tokens = Tokenizer(poem_content)
        self.random_assignment_tokens = Tokenizer(random_assignment_content)

    def test_word_tokenization(self):
        expected_tokens = [
            'march', 'abyss', 'look', 'acknowledge',
            'existence', 'live', 'life', 'full'
            ]
        word_tokens_poem = [str(token).lower() for token in list(self.poem_tokens.tokens_by_word)]
        self.assertListEqual(word_tokens_poem, expected_tokens)

    def test_wordpunct_tokenization(self):
        expected_tokens = [
            'march', 'abyss', '.', 'look', ',', 'acknowledge', 
            'existence', '.', 'live', 'life', 'full', '.'
            ]
        wordpunct_tokens_poem = [str(token).lower() for token in list(self.poem_tokens.tokens_by_wordpunct)]
        self.assertListEqual(wordpunct_tokens_poem, expected_tokens)

    def test_sentence_tokenization(self):
        expected_sentences = [
            'march into the abyss', 'look down,', 
            'acknowledge your existence', 'live your life at fullest'
            ]
        sentence_tokens_poem = [str(token).lower() for token in list(self.poem_tokens.tokens_by_sentence)]
        self.assertListEqual(sentence_tokens_poem, expected_sentences)

    def test_syntagm_tokenization(self):
        expected_syntagms = [
            ['march'], ['abyss'], ['look'], ['acknowledge'], 
            ['existence'], ['live'], ['life'], ['full']
            ]
        syntagm_tokens_poem = [[str(token).lower() for token in syntagm] for syntagm in self.poem_tokens.tokens_by_syntagm]
        self.assertEqual(len(syntagm_tokens_poem), len(expected_syntagms))
        for syntagm, expected in zip(syntagm_tokens_poem, expected_syntagms):
            self.assertListEqual(syntagm, expected)
    """
    def test_random_assigment(self):
        ... #TODO (but not really a priority right now)
    """

if __name__ == '__main__':
    unittest.main()