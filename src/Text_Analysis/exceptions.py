from .constants import MAX_SENT_LEN

class TokenListIsEmpty(Exception):
    def __init__(self, tokens_by):
        self.message = f"Warning: empty list of {tokens_by}: \nPlease make sure that there's data to work with."
        super().__init__(self.message)

class UnprocessableTextContent(Exception):
    def __init__(self, attribute) -> None:
        self.message = "Warning: the text can't be processed properly because: "
        possible_errors = {
            "tokens by syntagm": "tokens by syntagm list is empty, indicating the text is either not in English or only consists of stop words/punctuation.",
            "raw data": "raw data (e.g., the text extracted from a source file) is empty.",
            "text richness": "text richness is 1, meaning the text is either not in English or consists of entirely unique words (likely too short for analysis).",
            "average sentence length": f"sentences are too short on average to be considered valid. Minimum limit is {MAX_SENT_LEN} words/sentence."
        }
        self.message += possible_errors.get(attribute, attribute)
        super().__init__(self.message)