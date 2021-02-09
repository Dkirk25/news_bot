from pyrh import Robinhood
import pyotp
import os
import time
from datetime import date, timedelta
from dotenv import load_dotenv
from model.news import StockInfo
load_dotenv(override=True)


class StockHelper:
    def __init__(self):
        MFA = os.getenv("MFA")
        USERNAME = os.getenv("USERNAME")
        PASSWORD = os.getenv("PASSWORD")

        self._future_date = date.today() + timedelta(5)

        self._rh = Robinhood()
        self._rh.login(username=USERNAME,
                       password=PASSWORD,
                       qr_code=MFA)

    async def fetch_news(self, stock):
        stock_to_search = stock
        clean_stock_list = []
        if(self.is_time_to_reauthenticate(date.today())):
            self._rh.relogin_oauth2()

        try:
            news = self._rh.get_news(stock_to_search)
            info_results = news["results"]
            for i in info_results:
                stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                                       i["preview_text"].replace("\n\n", ""), i["url"], stock_to_search)
                # print(str(stock_info))
                clean_stock_list.append(stock_info)
            print(stock_to_search + " = " + str(len(clean_stock_list)))
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
