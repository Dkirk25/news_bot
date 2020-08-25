from pyrh import Robinhood
from model.news import StockInfo
import pyotp
import os
from pytz import timezone
from datetime import datetime
import unittest


class TestSum(unittest.TestCase):

    def test_stock_date_newer_than_discord(self):
        stock = datetime(2020, 8, 21, 15, 24, 33)
        test_date = datetime(
            2020, 8, 21, 17, 48, 49, 887000)

        print(stock)
        print(test_date)
        self.assertTrue(stock > test_date)


if __name__ == '__main__':
    unittest.main()
