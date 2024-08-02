import unittest
from TextAnalysis_AkaPhase1 import *
from random import choice

testfiles_path_basic = "../Resources/Sample Data/BasicTexts/"
testfiles_path_complex = "../Resources/Sample Data/ComplexTexts/"

class TestPhase1(unittest.TestCase):

    def setUp(self):
        self.poem_file = testfiles_path_basic + "poem1.txt"
        random_assignment_suffix = ["202", "211", "321"]
        self.random_assignment = testfiles_path_basic + "DataFromText-MiningProject/ass1-" + f"{choice(random_assignment_suffix)}" + ".txt"
        self.poem_tokens = Tokenizer(file=self.poem_file)
        self.random_assignment_tokens = Tokenizer(file=self.random_assignment)


    def test_word_tokenization(self):
        expected_tokens = ['march', 'abyss', 'look', 'acknowledge', 'existence', 'live', 'life', 'full']
        word_tokens_poem = list(self.poem_tokens.tokens_by_word)
        self.assertListEqual(word_tokens_poem, expected_tokens)

    def test_wordpunct_tokenization(self):
        expected_tokens = ['march', 'abyss', '.', 'look', ',', 'acknowledge', 'existence', '.', 'live', 'life', 'full', '.']
        wordpunct_tokens_poem = list(self.poem_tokens.tokens_by_wordpunct)
        self.assertListEqual(wordpunct_tokens_poem, expected_tokens)

    def test_sentence_tokenization(self):
        expected_sentences = ['march into the abyss', 'look down,', 'acknowledge your existence', 'live your life at fullest']
        sentence_tokens_poem = list(self.poem_tokens.tokens_by_sentence)
        self.assertListEqual(sentence_tokens_poem, expected_sentences)

    def test_syntagm_tokenization(self):
        expected_syntagms = [['march'], ['abyss'], ['look'], ['acknowledge'], ['existence'], ['live'], ['life'], ['full']]
        syntagm_tokens_poem = list(self.poem_tokens.tokens_by_syntagm)
        self.assertEqual(len(syntagm_tokens_poem), len(expected_syntagms))
        for syntagm, expected in zip(syntagm_tokens_poem, expected_syntagms):
            self.assertListEqual(list(syntagm), expected)

    def test_random_assigment(self):
        ... #TODO (but not really a priority right now)

if __name__ == '__main__':
    unittest.main()
