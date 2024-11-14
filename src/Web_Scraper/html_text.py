from dataclasses import dataclass
from requests import Response
from bs4 import BeautifulSoup

@dataclass
class HTMLText:
    response: Response

    def makeTempText(self) -> str:
        """
        Extracts meaningful text from HTML tags.
        """
        bs = BeautifulSoup(self.response.text, "html.parser")
        html_tags_list = bs.find_all({"h1", "h2", "h3", "p", "pre", "span"})
        return "\n".join([html_tag.get_text() for html_tag in html_tags_list])