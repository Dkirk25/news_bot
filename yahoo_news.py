import requests
from bs4 import BeautifulSoup
from datetime import datetime
from model.news import StockInfo
import os


class YahooHelper:
    def __init__(self):
        self.indicator = os.getenv("USE_ROBINHOOD", "N")
        self.parser = 'html.parser'

    def fetch_news(self, stock):
        url = f"https://finance.yahoo.com/quote/{stock}/?p={stock}"
        list_of_stock_info = []
        try:
            with requests.get(url, stream=True) as page:

                soup = BeautifulSoup(page.content, self.parser)

                #  Need to get the latest article
                latest_news_article = soup.find_all(
                    "div", class_="Ov(h) Pend(44px) Pstart(25px)")[0]

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

                published_at = self.get_time_of_article(news_url)

                stock_price = soup.find(
                    id="quote-header-info").contents[2].text
                if('+' in stock_price):
                    clean_price = stock_price.split('+')[0]
                else:
                    clean_price = stock_price.split('-')[0]
                stock_info = StockInfo(uuid, title, source, published_at,
                                       description, news_url, stock, clean_price)

                list_of_stock_info.append(stock_info)
        except Exception as ex:
            print("Error: ", ex, "Occurred with " + stock)

        return list_of_stock_info

    def get_time_of_article(self, new_url):
        page = requests.get(new_url)
        soup = BeautifulSoup(page.content, PARSER)

        return soup.time.text
