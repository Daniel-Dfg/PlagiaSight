#     __  ___ _  __
#    /  |/  /(_)/ /_   __  __ __  __
#   / /|_/ // // __ \ / / / // / / /
#  / /  / // // / / // /_/ // /_/ /
# /_/  /_//_//_/ /_/ \__,_/ \__,_/
#                       was here...
#
# refactored and OOP'd existing code

from .safe_search import SafeSearch
from .url_manager import URLs
from .html_text import HTMLText
from .utils import stopProcess
from .headers import headers

__all__ = [
    "SafeSearch",
    "URLs",
    "HTMLText",
    "stopProcess",
    "headers"
]