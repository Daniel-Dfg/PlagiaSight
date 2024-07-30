import unittest
from TextAnalysis_AkaPhase1 import *
from random import randint

testfiles_path_basic = "../Resources/Sample Data/BasicTexts/"
testfiles_path_complex = "../Resources/Sample Data/ComplexTexts/"

class TestPhase1(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.poem_file = testfiles_path_basic + "poem1.txt"
        # will need further explaination #TODO (don't try to understand this just yet, reader)
        random_assignment_suffix = ["202", "211", "321"]
        self.random_assignment = testfiles_path_basic + "DataFromText-MiningProject/ass1-" f"{random_assignment_suffix[randint(0,len(random_assignment_suffix))]}" + ".txt"
        self.poem_tokens = Tokenizer(file=self.poem_file)
        self.random_assignment_tokens = Tokenizer(file=self.random_assignment)
        super().__init__(methodName)

    def test_word_tokenization(self):
        expected_tokens = array(['march', 'abyss', 'look', 'acknowledge', 'existence', 'live', 'life', 'full'])
        word_tokens_poem = self.poem_tokens.tokens_by_word
        self.assertTrue(all(w1 == w2 for w1, w2 in zip(word_tokens_poem, expected_tokens)))

    def test_wordpunct_tokenization(self):
        expected_tokens = array(['march', 'abyss', '.', 'look', ',', 'acknowledge', 'existence', '.', 'live', 'life', 'full', '.'])
        wordpunct_tokens_poem = self.poem_tokens.tokens_by_wordpunct
        self.assertTrue(all(w1 == w2 for w1, w2 in zip(wordpunct_tokens_poem, expected_tokens)))

    def test_sentence_tokenization(self):
        expected_sentences = array(['march into the abyss', 'look down,', 'acknowledge your existence', 'live your life at fullest'])
        sentence_tokens_poem = self.poem_tokens.tokens_by_sentence
        self.assertTrue(all(s1 == s2 for s1, s2 in zip(sentence_tokens_poem, expected_sentences)))

    def test_syntagm_tokenization(self):
        expected_syntagms = [array(['march']), array(['abyss']), array(['look']), array(['acknowledge']), array(['existence']), array(['live']), array(['life']), array(['full'])]
        syntagm_tokens_poem = self.poem_tokens.tokens_by_syntagm
        self.assertTrue(len(syntagm_tokens_poem) == len(expected_syntagms))
        self.assertTrue(all(w1 == w2 for w1, w2 in zip(syntagm_tokens_poem, expected_syntagms)))

    def test_random_assigment(self):
        ... #TODO

if __name__ == '__main__':
    unittest.main()
