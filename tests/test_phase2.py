import pytest
import os # To be used in the future for the error handling
import unittest
from src import URLs, HtmlText

class TestScraping(unittest.TestCase):
    def setUp(self):
        x = URLs("spear", 3)
        self.p = x.response_array
        self.temp = HtmlText(self.p[0])

    def extract_temp_data(self):
        with open("../data/temp.txt", "r", encoding="utf-8-sig") as file:
            self.temp_content = file.read()
        return self.temp_content
    """
    def test_temp(self):

        data = self.extract_temp_data()

        if self.assertTrue(data):
            for i in range(1, len(self.p)):
                self.temp.removeTempText()
                self.temp = HtmlText(self.p[i])
        else:
            self.assertTrue(data)
    """
    """
    To be done because allowed_chars it not that simple
    if any(char not in allowed_chars for char in data):
        raise Exception("Invalid characters found in temp file")
    """
