from datetime import date, timedelta, datetime
from stock_helper import StockHelper
import unittest
import sys

stock_helper = StockHelper()


class TestSum(unittest.TestCase):

    def test_current_date(self):
        today = date.today()
        actual = stock_helper.is_time_to_reauthenticate(today)

        self.assertFalse(actual)

    def test_stock_date_newer_than_discord(self):
        stock = datetime(2020, 8, 21, 15, 24, 33)
        test_date = datetime(
            2020, 8, 21, 17, 48, 49, 887000)

        print(stock)
        print(test_date)
        self.assertTrue(stock < test_date)

    def test_fetch_WHKS_news(self):
        news = []
        news = stock_helper.fetch_news("WKHS")

        print(news)
        self.assertIsNotNone(news)


if __name__ == '__main__':
    unittest.main()
