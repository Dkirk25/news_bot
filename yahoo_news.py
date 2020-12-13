import requests
from bs4 import BeautifulSoup
from datetime import datetime


PARSER = 'html.parser'

# https://finance.yahoo.com/quote/WKHS/news?p=WKHS

def get_news(stock):
    url = 'https://finance.yahoo.com/quote/WKHS/news?p=' + stock
    page = requests.get(url)
    soup = BeautifulSoup(page.content, PARSER)

    latest_news_article = soup.find(id="latestQuoteNewsStream-0-Stream").contents[0].contents[0]

    # Description latest_news_article.p.text

    # Title latest_news_article.h3.text

    # source latest_news_article.h3.previous

    #time latest_news_article.contents[0].contents[0].contents[0].contents[0]

    return []