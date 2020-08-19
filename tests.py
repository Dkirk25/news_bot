from pyrh import Robinhood
from model.news import StockInfo
import pyotp
import os
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


def fetch_news():
    stock_to_search = "WKHS"
    news = rh.get_news(stock_to_search)
    info_results = news["results"]
    clean_stock_list = []
    for i in info_results:
        stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                               i["preview_text"].replace("\n\n", ""), i["url"], stock_to_search)
        clean_stock_list.append(stock_info)
    return clean_stock_list


class TestSum(unittest.TestCase):

    def test_robinhood_new_ouput(self):
        list_of_stock_info = fetch_news()
        self.assertEqual(list_of_stock_info[0].stock_name, "WKHS")


if __name__ == '__main__':
    unittest.main()
