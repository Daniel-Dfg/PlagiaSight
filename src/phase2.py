"""
    Coded by: Luckyyyin and Daniel-Dfg
"""
from bs4 import BeautifulSoup
from googlesearch import search
from requests import get
from numpy import array
from nltk import clean_html
from dataclasses import field, dataclass

@dataclass
class URLs:
    """
        ## Parameters
        
            word : str
                search word
            number : int 
                Number of Urls within the array
        
        ## Functions
        
            url_array() -> array[str]
                returns an numpy array of url string equal to the number given 
        
        ## Example
        
            >>> x = URLs("football", 3)
            >>> x.url_array
            ["http//:www.football.com", "http//:www.footballworld.com", "http//:www.worldcup.com"]
    """
    
    wordsent: str
    number: int
    _url_array: array = field(init=False)
    
    def __post_init__(self):
        self.makeUrls()
        
    def makeUrls(self):
        self.url_array(search(self.wordsent, num=self.number, stop=self.number))
    
    @property
    def url_array(self) -> array:
        if self._url_array.size == 0:
            print("Warning: url array is empty")
        return self._url_array
        
@dataclass
class HtmlText:
    """
        ## Parameters
        
            url : str
                website url
        
        ## Functions
        
            text() -> str
                returns a text string from the url html file
        
        ## Example
        
            >>> x = HtmlText("http//:worldcup.com")
            >>> x.text()
            "The world cup 2024 was ..."
    """
    
    url: str
    _html_text : str = field(init= False)
    
    def __post_init__(self):
        self.makeText()
        
    def makeText(self): #TODO solve Error with complexes sites structure
        html = get(self.url).text
        bs = BeautifulSoup(html, "html5lib")
        self._html_text = bs.find_all().encode('utf-8-sig')
        
    @property
    def html_text(self):
        return self._text

x = HtmlText("https://www.w3schools.com/")
print(x)

