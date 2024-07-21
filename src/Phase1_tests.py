import unittest
from TextAnalysis_AkaPhase1 import *
from numpy import array
\
testfiles_path_basic = "../Resources/Sample Data/BasicTexts/"
testfiles_path_complex = "../Resources/Sample Data/ComplexTexts/"

class TestPhase1(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.poem_file = testfiles_path_basic + "poem1.txt"
        self.random_assignment = testfiles_path_basic + "DataFromText-MiningProject/ass1-202.txt"
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

if __name__ == "__main__":
    unittest.main()



    
    
    """def test_word_count(self):
        text = "This is a sample text."
        analysis = TextAnalysis_AkaPhase1(text)
        self.assertEqual(analysis.word_count(), 5)

    def test_unique_words(self):
        text = "This is a sample text. This is another sample text."
        analysis = TextAnalysis_AkaPhase1(text)
        self.assertEqual(analysis.unique_words(), 6)

    def test_most_common_words(self):
        text = "This is a sample text. This is another sample text."
        analysis = TextAnalysis_AkaPhase1(text)
        self.assertEqual(analysis.most_common_words(2), [("sample", 2), ("this", 2)])

    def test_longest_word(self):
        text = "This is a sample text."
        analysis = TextAnalysis_AkaPhase1(text)
        self.assertEqual(analysis.longest_word(), "sample")

    def test_word_frequency(self):
        text = "This is a sample text. This text contains repeated words."
        expected_frequency = {'This': 2, 'is': 1, 'a': 1, 'sample': 1, 'text': 2, 'contains': 1, 'repeated': 1, 'words': 1}
        actual_frequency = TextAnalysis_AkaPhase1.word_frequency(text)
        self.assertEqual(actual_frequency, expected_frequency)"""


if __name__ == '__main__':
    unittest.main()