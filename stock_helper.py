from pyrh import Robinhood
import pyotp
import os
import time
from datetime import date, timedelta
from dotenv import load_dotenv
from model.news import StockInfo
import json
import decimal
load_dotenv(override=True)

MFA = os.getenv("MFA")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


class StockHelper:
    def __init__(self):
        self._future_date = date.today() + timedelta(5)

        self._rh = Robinhood()
        self._rh.login(username=USERNAME,
                       password=PASSWORD,
                       qr_code=MFA)

    def fetch_news(self, stock):
        stock_to_search = stock
        clean_stock_list = []
        if(self.is_time_to_reauthenticate(date.today())):
            self._rh.login(username=USERNAME,
                           password=PASSWORD,
                           qr_code=MFA)

        try:
            news = self._rh.get_news(stock_to_search)
            info_results = news["results"]

            for i in info_results:
                TWOPLACES = decimal.Decimal(10) ** -2
                price = str(
                    self._rh.last_trade_price(stock)[0][0])

                stock_price = str(decimal.Decimal(price).quantize(TWOPLACES))
                print(stock_price)
                stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                                       i["preview_text"].replace("\n\n", ""), i["url"], stock_to_search, stock_price)
                clean_stock_list.append(stock_info)
            print(stock_to_search + " = " + str(clean_stock_list[0]))
        except Exception as e:
            print("Error: ", e, "Occurred.")
            print("Skipping...")
            print()
        return clean_stock_list

    def is_time_to_reauthenticate(self, now):
        if(now == self._future_date):
            self._future_date = date.today() + timedelta(5)
            return True
        return False
