from requests import get, RequestException, Response, ReadTimeout, ConnectionError, HTTPError
from numpy import array, ndarray, append, zeros
from urllib.robotparser import RobotFileParser
from http.client import RemoteDisconnected
from dataclasses import field, dataclass
from duckduckgo_search import DDGS
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from subprocess import run
from sys import platform
from time import sleep
from os import remove

# Important for safe and sure scraping
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', # name of the app
           'Accept': 'text/html', # wanted file
           'Accept-Encoding': 'gzip, deflate, br', # accept compression
           'Accept-Language': 'en', # used language
           'DNT': '1', # do not track (if possible)
           'Upgrade-Insecure-Requests': '1', # Upgrade request https if possible
           'Cache-Control': 'no-cache'}

@dataclass
class URLs:
    """
        # Create an array of urls
    """
    word_sent: str
    number: int
    useless_domain: str = field(init=False, repr=False) # Exclude useless domain
    _url_array: ndarray = field(init=False, repr=False)
    _response_array: ndarray = field(init=False, repr=False)
    #TODO dict store url infos: response, title, author, date, co-author, etc...

    def __post_init__(self):
        self.useless_domain = "-site:amazon.com -site:ebay.com -site:tiktok.com -site:youtube.com -site:netflix.com -site:facebook.com -site:twitter.com -site:instagram.com -site:hulu.com -site:amazon.jobs -site:indeed.com"
        self._url_array = self.makeUrls(f"{self.word_sent} {self.useless_domain}", self.number)
        self._response_array = zeros(self.number, dtype=Response)
        self.recycleUrls()

    @staticmethod
    def makeUrls(word_sent:str, number:int, start:int =0) -> ndarray:
        """
            # google: Avoid error 429 (Too many requests) and ddgo: Avoid error 202 Ratelimit
            # Solution using multi proxy ports and search engines
            # And search limit search per word_sent max 10
        """
        ddgo = DDGS(headers=headers)
        results = ddgo.text(word_sent, max_results=number)
        urls = [result['href'] for result in results][start:]
        return array(urls, dtype="S150")

    @staticmethod
    def manageRobotsDotTxt(url:bytes) -> bool:
        """
            - Get robots.txt file from the url site and check if it's allowed to scrape
        """
        parsed_url = urlparse(url.decode())
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        rfp = RobotFileParser()
        rfp.set_url(robots_url)
        try:
            rfp.read() # Read robots.txt
        except (UnicodeDecodeError, RemoteDisconnected, RequestException): # No robots.txt
            return True
        return rfp.can_fetch(headers["User-Agent"], url)  # Check if "plaigaLand" is allowed to scrap the url

    def recycleUrls(self) -> None:
        """
        - Filter replace urls that are {unreachable, not allowed to scrape and with errors} with new functional urls.
        # TODO better error solving
        """
        cut_at:int = self.number # start at none seen url
        response: Response
        start_cycle = self.number+1
        count = 0
        while self.number:
            for url in self._url_array[cut_at-self.number:]:
                try:
                    response = get(url, headers=headers, timeout=2)
                    response.raise_for_status()
                    print(response)
                    print(url)
                    sleep(1)
                except (ReadTimeout, ConnectionError, HTTPError):
                    print("Unreachable website")
                    response.status_code = 0
                if response.status_code == 200 and self.manageRobotsDotTxt(url): # Checks for vaild website
                    self._response_array[count] = response
                    count +=1
                    self.number -=1
                else:
                    unwanted = self._url_array != url
                    self._url_array = self._url_array[unwanted] # Remove unwanted url from array
            if self.number:
                new_urls = self.makeUrls(f"{self.word_sent} {self.useless_domain}", self.number+start_cycle, start_cycle)
                start_cycle += self.number
                self._url_array = append(self._url_array, new_urls)

    @property
    def url_array(self) -> ndarray:
        if self._url_array.size == 0:
            print("Warning: url array is empty")
        return self._url_array
    
    @property
    def response_array(self) ->ndarray:
        if self._response_array.size == 0:
            print("Warning: url array is empty")
        return self._response_array

@dataclass
class HtmlText:
    """
        # Create a temporary text file from url site html text
    """

    response: Response

    def __post_init__(self):
        self.makeTempText()


    def makeTempText(self):
        """
            TODO (or not): How to manage sites with multilayer/pages
        """
        try:
            self.response.raise_for_status()
            bs = BeautifulSoup(self.response.text, "html.parser")
            html_tags_list = bs.find_all(["h1", "h2", "h3", "p", "pre"]) # Get good part of any info site (ideal of an info site)
            with open("temp.txt", "w", encoding="utf-8-sig") as t:
                for html_tag in html_tags_list:
                    t.write(html_tag.get_text()+"\n") # Transform each tag to a text and write it in the temp file
        except RequestException:
            print("Response error")

    def removeTempText(self): # To discuss (whether temp file or straight up str)
        remove("temp.txt")



class UserStatus:
    """
        Improve user experience, manage status, internet connection, etc...
    """

    @staticmethod
    def check_wifi_connection_linux():
        """
            #TODO check wifi status for mac and windows
        """
        try:
            if platform == "linux" or platform == "linux2":
                result = run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
            elif platform == "darwin":
                # OS X
                pass
            elif platform == "win32":
                # Windows
                pass
            if result.returncode == 0:
                output = result.stdout.strip().split('\n')
                connected_network = next((line.split(':')[1] for line in output if line.startswith('yes:')), None)
                if connected_network:
                    print("Wi-Fi is connected")
                    print(f"Connected to: {connected_network}")
                else:
                    print("Wi-Fi is not connected")
            else:
                print("Failed to retrieve Wi-Fi status")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def check_for_response():# TODO run in parallel every 5 sec
        """
            - Goal prevent problems when there is no internet connection
            # TODO run in parallel (and when requests and googlescreach)
            # TODO manage internet connection errors more efficently, know what every response means.
        """
        response = get("example.com", headers=headers, timeout=2)
        if response.status_code == 200:
            print("OK for internet connection")
        else:
            print("No internet connection")

    @staticmethod
    def save_changes(): # To discuss
        """
            # Create/change file json, if user changes the settings, perfrence, etc...
        """
        pass
    @staticmethod
    def user(): # To discuss
        """
            # Getting the user name/info for legal accusation (just in case :x)
        """
        pass

#x = URLs("spear", 10)
#p = x.response_array
#temp = HtmlText(p[0])
#temp.removeTempText()
