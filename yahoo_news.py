import requests
from bs4 import BeautifulSoup
from datetime import datetime
from model.news import StockInfo


PARSER = 'html.parser'

# https://finance.yahoo.com/quote/WKHS/news?p=WKHS

def get_news(stock):
    url = f"https://finance.yahoo.com/quote/{stock}/news?p={stock}"
    with requests.get(url, stream=True) as page:

        # page = requests.get(url)
        soup = BeautifulSoup(page.content, PARSER)

        latest_news_article = soup.find(id="latestQuoteNewsStream-0-Stream").contents[0].contents[0]

        uuid = latest_news_article.h3.next['data-uuid']

        # Description latest_news_article.p.text
        list_of_sentences = latest_news_article.p.text.split(". ")
        description = '. '.join(list_of_sentences[0:2])

        # Title latest_news_article.h3.text
        title = latest_news_article.h3.text

        # source latest_news_article.h3.previous
        source = latest_news_article.h3.previous

        source_url = latest_news_article.h3.next['href']
        news_url = 'https://finance.yahoo.com' + source_url

        published_at = get_time_of_article(news_url)

        stock_info = StockInfo(uuid, title, source, published_at,
                                    description, news_url, stock)

        return stock_info




def get_time_of_article(new_url):
    page = requests.get(new_url)
    soup = BeautifulSoup(page.content, PARSER)

    return soup.time.text
