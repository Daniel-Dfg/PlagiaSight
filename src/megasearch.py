from duckduckgo_search import DDGS
from googlesearch import search
from time import sleep
from random import randint

def megaSearch(word_sent, number,cooldown, headers=None, start=0):
    while True:
        try:
            if not cooldown[0]:
                ddgo = DDGS(headers=headers)
                results = ddgo.text(word_sent, max_results=number)
                urls = [result['href'] for result in results][start:]
                sleep(2)
                return urls
        except:
            print("1 donwn")  
            cooldown[0] = True
        try:
            urls = list(search(word_sent, num=number, stop=number, start=start, pause=2, user_agent=headers["User-Agent"]))
            return urls
        except:
            givePenalty()
            cooldown[0] = False

def givePenalty():
    print("5 min penalty")
    sleep(20)
    print("Nah...")
    sleep(20)
    print("You're kidding right?!")
    sleep(20)
    print("This is search engines a abuse...")
    sleep(60)
    print("What are you even searching?")
    sleep(60)
    print("A Whale?!")
    sleep(60)
    print("Be patient only one minute")
    sleep(60)