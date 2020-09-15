from pyrh import Robinhood
from model.news import StockInfo
import database
import pyotp
import os
from pytz import timezone
from model.news import StockInfo
from pyrh import Robinhood
import pyotp
from datetime import datetime
import unittest
from dotenv import load_dotenv
load_dotenv(override=True)

MFA = os.getenv("MFA")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

totp = pyotp.TOTP(MFA).now()
rh = Robinhood()
rh.login(username=USERNAME,
         password=PASSWORD,
         qr_code=MFA)


def fetch_news(stock):
    stock_to_search = stock
    news = rh.get_news(stock_to_search)
    info_results = news["results"]
    clean_stock_list = []
    for i in info_results:
        stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                               i["preview_text"].replace("\n\n", ""), i["url"], stock_to_search)
        print(str(stock_info))
        clean_stock_list.append(stock_info)
    return clean_stock_list


class TestSum(unittest.TestCase):

    def test_stock_date_newer_than_discord(self):
        stock = datetime(2020, 8, 21, 15, 24, 33)
        test_date = datetime(
            2020, 8, 21, 17, 48, 49, 887000)

        print(stock)
        print(test_date)
        self.assertTrue(stock < test_date)

    def test_fetch_WHKS_news(self):
        news = []
        news = rh.get_news("WKHS")

        print(news)


if __name__ == '__main__':
    unittest.main()
