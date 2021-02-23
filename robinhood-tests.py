from pyrh import Robinhood
from model.news import StockInfo
import database
import pyotp
import os
from pytz import timezone
from pyrh import Robinhood
import pyotp
from datetime import datetime
from stock_helper import StockHelper
import unittest
import sys
from dotenv import load_dotenv
load_dotenv(override=True)

MFA = os.getenv("MFA")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

rh = Robinhood()
rh.login(username=USERNAME,
         password=PASSWORD,
         qr_code=MFA)


def fetch_news(stock):
    stock_to_search = stock
    clean_stock_list = []
    try:
        news = rh.get_news(stock_to_search)
        info_results = news["results"]
        for i in info_results:
            stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                                   i["preview_text"].replace("\n\n", ""), i["url"], stock_to_search)
            print(str(stock_info))
            clean_stock_list.append(stock_info)
    except Exception as e:
        print("Error: ", e.__class__, "Occurred.")
        print()
    return clean_stock_list


class TestSum(unittest.TestCase):

    def test_fetch_WHKS_news(self):
        news = []
        news = fetch_news("TSLA")[0]

        print(news)
