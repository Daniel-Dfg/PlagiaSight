from time import sleep
from requests import get, ConnectionError

def stopProcess() -> None:
    """
    Loops until the internet connection is back.
    """
    while True:
        sleep(2)
        try:
            get("https://example.com")
        except ConnectionError:
            print("No Internet connection")
            continue
        return