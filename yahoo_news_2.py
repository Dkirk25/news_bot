import yfinance

from model.news import StockInfo
from store_decoder import StoreDecoder

decoder = StoreDecoder()


class YahooHelper2:
    def __init__(self):
        self.parser = 'lxml'

    def fetch_news(self, stock_name):
        list_of_stock_info = []
        try:
            stock_result = yfinance.Ticker(str(stock_name))
            stock = stock_result.news[0]
            stock_info = self.yahoo_get_news_results(stock, stock_result.info, stock_name)
            list_of_stock_info.append(stock_info)
        except Exception as ex:
            print("Error: ", ex, "Occurred with " + stock)

        return list_of_stock_info

    # def get_time_of_article(self, new_url, header):
    #     try:
    #         with requests.get(new_url, stream=True, headers=header) as page:
    #             soup = BeautifulSoup(page.content, self.parser)
    #             return soup.time.text
    #     except Exception as ex:
    #         print("Error: ", ex, "Could not process request: " + new_url)
    #         current_timestamp = datetime.now()
    #         return datetime.strftime(current_timestamp, '%B %d, %Y, %I:%M %p')
    #
    # def yahoo_get_header_stock_data(self, matched_string_json):
    #     return list(dict(decoder.decode_store(matched_string_json)['QuoteSummaryStore']['price'][
    #                          'regularMarketPrice']).values())[0]

    def yahoo_get_news_results(self, stock, info, stock_name):

        uuid = stock['uuid']
        title = stock['title']
        # summary = stock['summary']
        source = stock['publisher']
        # original_publication_url = stock['url']
        yahoo_url = f"{stock['link']}"

        stock_price = info["currentPrice"]

        published_at = stock['providerPublishTime']

        return StockInfo(uuid, title, source, published_at, yahoo_url,
                         stock_name, stock_price)
