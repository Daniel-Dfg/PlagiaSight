import unittest
import TextAnalysis_AkaPhase1


testfiles_path_basic = "../Resources/Sample Data/BasicTexts/"
testfiles_path_complex = "../Resources/Sample Data/ComplexTexts/"
class TestPhase1(unittest.TestCase):
    def test_word_count(self):
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
        self.assertEqual(actual_frequency, expected_frequency)


if __name__ == '__main__':
    unittest.main()