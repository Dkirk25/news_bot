from model.news import StockInfo
from pytz import timezone
from model.news import StockInfo
from datetime import datetime
import unittest
import sys
import stock_helper

class TestSum(unittest.TestCase):
    def test_fetch_WHKS_news(self):
        news = []
        news = stock_helper.fetch_news("GEVO")

        print(news)


if __name__ == '__main__':
    unittest.main()
