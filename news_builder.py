
from stock_helper import StockHelper
from yahoo_news import YahooHelper
import os
from dotenv import load_dotenv
load_dotenv(override=True)


class NewsBuilder:
    def __init__(self):
        self.indicator = os.getenv("USE_ROBINHOOD", "N")

    def get_news_helper(self):
        if self.indicator == "Y":
            return StockHelper()
        elif self.indicator == "N":
            return YahooHelper()
        else:
            return ValueError(indicator)
