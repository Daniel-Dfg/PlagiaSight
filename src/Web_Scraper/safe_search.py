from dataclasses import dataclass, field
from time import sleep
from urllib.error import URLError

from googlesearch import search
from requests import HTTPError

from .utils import stopProcess

@dataclass
class SafeSearch:
    phrases: list[str] = field(init=False, repr=False)

    def __post_init__(self):
        self.phrases = [
            "5 min penalty", "Nah...", "You're kidding right?!",
            "This is search engines abuse...", "What are you even searching?",
            "A Whale?!", "Be patient only one minute"
        ]

    def givePenalty(self) -> None:
        """
        Timeout when HTTP requests reach search engine limits.
        """
        for phrase in self.phrases:
            print(phrase)
            sleep(30)

    def safeSearch(self, word_sent: str, number: int, user=None, start=0) -> list:
        """
        Combines search engine results with a safety mechanism.
        """
        while True:
            try:
                urls = list(search(word_sent, num=number, stop=number, start=start, user_agent=user))
                return urls
            except HTTPError:
                self.givePenalty()
                continue
            except URLError:
                stopProcess()
                continue