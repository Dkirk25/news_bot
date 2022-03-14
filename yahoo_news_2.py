import requests
from bs4 import BeautifulSoup
from datetime import datetime
from model.news import StockInfo
import json
import re


class YahooHelper2:
    def __init__(self):
        self.parser = 'lxml'

    def fetch_news(self, stock):
        url = f"https://finance.yahoo.com/quote/{stock}/news?p={stock}"
        list_of_stock_info = []
        header = {'Connection': 'keep-alive',
                  'Expires': '-1',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                  }
        try:
            with requests.get(url, stream=True, headers=header) as page:

                soup = BeautifulSoup(page.content, self.parser)

                all_script_tags = soup.select('script')

                # https://regex101.com/r/IJloEU/2
                matched_string = ''.join(re.findall(
                    r'root\.App\.main = (.*);\n+}\(this\)\);\n+</script>', str(all_script_tags)))
                matched_string_json = json.loads(matched_string)

                stock_info = self.yahoo_get_news_results(stock,
                                                         matched_string_json, header)
                list_of_stock_info.append(stock_info)
        except Exception as ex:
            print("Error: ", ex, "Occurred with " + stock)

        return list_of_stock_info

    def get_time_of_article(self, new_url, header):
        try:
            with requests.get(new_url, stream=True, headers=header) as page:
                soup = BeautifulSoup(page.content, self.parser)
                return soup.time.text
        except Exception as ex:
            print("Error: ", ex, "Could not process request: " + new_url)
            current_timestamp = datetime.now()
            return datetime.strftime(current_timestamp, '%B %d, %Y, %I:%M %p')

    def yahoo_get_header_stock_data(self, matched_string_json):
        return list(dict(matched_string_json['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']).values())[0]

    def yahoo_get_news_results(self, stock, matched_string_json, header):
        name_stock_mega = list(
            matched_string_json['context']['dispatcher']['stores']['StreamStore']['streams'])[0]
        yahoo_news_index = matched_string_json['context']['dispatcher']['stores'][
            'StreamStore']['streams'][name_stock_mega]['data']['stream_items'][0]
        uuid = yahoo_news_index['id']
        title = yahoo_news_index['title']
        summary = yahoo_news_index['summary']
        source = yahoo_news_index['publisher']
        original_publication_url = yahoo_news_index['url']
        yahoo_url = f"https://finance.yahoo.com{yahoo_news_index['link']}"

        stock_price = str(self.yahoo_get_header_stock_data(
            matched_string_json))

        published_at = self.get_time_of_article(yahoo_url, header)

        return StockInfo(uuid, title, source, published_at,
                         summary, original_publication_url, stock, stock_price)
