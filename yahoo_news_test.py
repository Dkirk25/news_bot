from model.news import StockInfo
import unittest
import yahoo_news


class TestSum(unittest.TestCase):

    def test_fetch_WHKS_news(self):
        news = []
        news = yahoo_news.get_news("WKHS")

        print(news)
        self.assertEqual("horse -9% with USPS said to delaying big contract decision", news)


if __name__ == '__main__':
    unittest.main()