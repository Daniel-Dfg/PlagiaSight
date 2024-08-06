# 2024 Copyright ©
from urllib.robotparser import RobotFileParser
from requests import get, exceptions, Response
from dataclasses import field, dataclass
from numpy import array, ndarray, append
from urllib.parse import urlparse
from googlesearch import search
from bs4 import BeautifulSoup
from subprocess import run
from sys import platform
from time import sleep
from os import remove

headers = {'User-Agent': 'Plagialand'} # To discuss

@dataclass
class URLs:
    """
        # Create an array of urls
    """
    word_sent: str
    number: int
    #Exclude useless domain
    useless_domain: str = field(init=False, repr=False)
    _url_array: ndarray = field(init=False, repr=False)

    def __post_init__(self):
        self.useless_domain = "-site:amazon.com -site:ebay.com -site:tiktok.com -site:youtube.com -site:netflix.com -site:facebook.com -site:twitter.com -site:instagram.com -site:hulu.com"
        self._url_array = self.makeUrls(f"{self.word_sent} {self.useless_domain}", self.number, self.number)
        self.recycleUrls()

    @staticmethod
    def makeUrls(word_sent:str, number:int, end:int, begin:int=0) -> ndarray:
        """
            # TODO filter unreachable url (garpage code)
            # TOCHECK (it seems that googlesearch has a limited number of http requests)
            # Avoid error 429 (Too many requests)
            # TODO Find better search methode than google
        """
        return array(list(search(word_sent, num=number, stop=end, start=begin, pause=0.5)), dtype="U100")

    @staticmethod
    def manageRobotsDotTxt(url:str) -> bool:
        """
            - Get robots.txt file from the url site and check if it's allowed to scrape
            # To disscus if reponse is false:
                1) Forget the url and find another one, using later on using URLs class (better option)
                2) Allow but at the user risque, taking the full responsiblity

        """
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        rfp = RobotFileParser()
        rfp.set_url(robots_url)
        rfp.read()# Read robots.txt
        return rfp.can_fetch(headers["User-Agent"], url)  # Check if "plaigaland" is allowed to scrap the url

    def recycleUrls(self) -> None:
        """
        - Filter replace urls that are {unrechable, not allowed to scrape and with errors} with new functional urls.
        # TODO better error solving
        """
        cut_at:int = self.number # start at none seen url
        response: Response
        start_cycle = self.number+1
        while self.number:
            for url in self._url_array[cut_at-self.number:]:
                try:
                    response = get(url)
                    response.raise_for_status()
                    print(response)
                    sleep(0.5)
                except:
                    print("error")
                    response.status_code = 0
                if response.status_code == 200 and self.manageRobotsDotTxt(url): # Checks for vaild website
                    self.number -=1
                else:
                    unwanted = self._url_array != url
                    self._url_array = self._url_array[unwanted] # Remove unwanted url from array
            if self.number:
                new_urls = self.makeUrls(f"{self.word_sent} {self.useless_domain}", self.number, self.number, start_cycle)
                start_cycle += self.number
                self._url_array = append(self._url_array, new_urls)

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

    def __post_init__(self):
        self.makeTempText()


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
x = URLs("football", 10)
print(x.url_array)
