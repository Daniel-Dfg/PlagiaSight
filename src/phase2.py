# 2024 Copyright ©
from urllib.robotparser import RobotFileParser
from dataclasses import field, dataclass
from urllib.parse import urlparse
from numpy import array, ndarray
from googlesearch import search
from bs4 import BeautifulSoup
from subprocess import run
from sys import platform
from requests import get
from os import remove

headers = {'User-Agent': 'MyScraper '} # To discuss

@dataclass
class URLs:
    """
        # Create an array of urls
    """

    word_sent: str
    number: int
    # To discuss (wheither inculde useful domain or exclude useless domain)
    useless_domain: str = "-site:amazon.com -site:ebay.com -site:tiktok.com -site:youtube.com -site:netflix.com"
    _url_array: ndarray = field(init=False, repr=False)

    def __post_init__(self):
        self.makeUrls()

    def makeUrls(self):
        """
            # TODO filter unreachable url (garpage code)
            # TOCHECK (it seems that googlesearch has a limited number of http requests)
            # Avoid error 429 (Too many requests)
        """
        self._url_array = array(list(search(f"{self.word_sent} {self.useless_domain}", num=self.number, stop=self.number, pause=1)), dtype="U100")

    @property
    def url_array(self) -> ndarray:
        if self._url_array.size == 0:
            print("Warning: url array is empty")
        return self._url_array

@dataclass
class HtmlText:
    """
        #Create a temporary text from site html
    """

    url: str
    response: bool

    def __post_init__(self):
        self.manage_robots_txt()
        if self.response:
            self.makeTempText()
        else:
            print("scraping is not allowed")

    def manageRobotsDotTxt(self):# I think it would be more efficient in URLs class :|
        """
            check the robots.txt file in site if it's allow to scrape
            #TODO if reponse is false: To disscus
                1) Forget the url and find another one, using later on using URLs class (better option)
                2) Allow but at the user risque, taking the full responsiblity

        """
        base_url = "https://" + urlparse(self.url).netloc + "/robots.txt"
        rp = RobotFileParser()
        rp.set_url(base_url)
        self.response = rp.can_fetch("*",self.url)

    def makeTempText(self):
        """
            TODO (or not): How to manage sites with multilayer/pages
        """
        response = get(self.url, headers=headers)
        if response.status_code == 200: # OK response
            bs = BeautifulSoup(response.text, "html.parser")
            html_tags_list = bs.find_all(["h1", "h2", "h3", "p"]) # Get good part of any info site (ideal of an info site)
            with open("temp.txt", "w", encoding="utf-8-sig") as t:
                for html_tag in html_tags_list:
                    t.write(html_tag.get_text()) # Tansform each tag to a text and write it in the temp file
        else:
            print(f'error code {response}')

    def removeTempText(self): # To discuss (wheither temp file or stright up str)
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
        response = get("example.com")
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
