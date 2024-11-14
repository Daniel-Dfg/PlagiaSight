from string import punctuation

# Global constants
VALID_FILE_EXTENSIONS = [".txt"]
REGEX_SPLIT_SENTENCES = r"(?<!\w\.\w.)(?<!\b[A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?)\s|\n"
MAX_TEXT_LEN = 3    # Minimal number of sentences for analysis
MAX_SENT_LEN = 3    # Minimal average words per sentence
TIME = None
CUSTOM_PUNCTUATION = set(punctuation + '•"“”')