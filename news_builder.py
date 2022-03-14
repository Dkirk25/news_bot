
from robinhood_helper import RobinhoodHelper
from yahoo_news_2 import YahooHelper2
import os
from dotenv import load_dotenv
load_dotenv(override=True)


class NewsBuilder:
    def __init__(self):
        self.indicator = os.getenv("USE_ROBINHOOD", "Y")

    def get_news_helper(self):
        if self.indicator == "Y":
            return RobinhoodHelper()
        elif self.indicator == "N":
            return YahooHelper2()
        else:
            return ValueError(self.indicator)
