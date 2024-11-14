from dataclasses import dataclass, field
from time import sleep
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

from numpy import array, append, zeros, ndarray
from requests import get, Response
from requests.exceptions import ReadTimeout, ConnectTimeout, ConnectionError, RequestException

from .headers import headers
from .safe_search import SafeSearch
from .utils import stopProcess

ss = SafeSearch()  # Initialize SafeSearch

@dataclass
class URLs:
    word_sent: str
    number: int
    useless_domain: str = field(init=False, repr=False)
    _response_array: ndarray = field(init=False, repr=False)

    def __post_init__(self):
        self.useless_domain = "-site:amazon.com -site:ebay.com -site:tiktok.com -site:youtube.com -site:netflix.com -site:facebook.com -site:twitter.com -site:instagram.com -site:hulu.com -site:amazon.jobs -site:indeed.com -site:bpost.be -site:postpack.ca"
        self._url_array = self.makeUrls(f"{self.word_sent} {self.useless_domain}", self.number)
        self._response_array = zeros(self.number, dtype=Response)
        self.recycleUrls()

    @staticmethod
    def makeUrls(word_sent: str, number: int, start: int = 0) -> ndarray:
        urls = ss.safeSearch(word_sent, number, headers["User-Agent"], start)
        return array(urls)

    @staticmethod
    def manageRobotsDotTxt(url: str) -> bool:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        rfp = RobotFileParser()
        rfp.set_url(robots_url)

        while True:
            try:
                rfp.read()
            except (UnicodeDecodeError, RequestException):
                return True
            except URLError:
                stopProcess()
                continue
            return rfp.can_fetch(headers["User-Agent"], url)

    def recycleUrls(self) -> None:
        cut_at: int = self.number
        start_cycle = self.number + 1
        count = 0

        while self.number:
            for url in self._url_array[cut_at - self.number:]:
                while True:
                    try:
                        response = get(url, headers=headers, timeout=2)
                        sleep(2)
                        break
                    except (URLError, ReadTimeout, ConnectTimeout):
                        response = Response()
                        response.status_code = 0
                        break
                    except ConnectionError:
                        stopProcess()
                        continue

                if response.status_code == 200 and self.manageRobotsDotTxt(url):
                    self._response_array[count] = response
                    count += 1
                    self.number -= 1
                else:
                    self._url_array = self._url_array[self._url_array != url]

            if self.number:
                new_urls = self.makeUrls(f"{self.word_sent} {self.useless_domain}", self.number, start_cycle)
                start_cycle += self.number
                self._url_array = append(self._url_array, new_urls)

    @property
    def url_array(self) -> ndarray:
        if self._url_array.size == 0:
            print("Warning: URL array is empty")
        return self._url_array

    @property
    def response_array(self) -> ndarray:
        if self._response_array.size == 0:
            print("Warning: response array is empty")
        return self._response_array