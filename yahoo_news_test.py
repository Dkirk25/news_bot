from model.news import StockInfo
import unittest
import yahoo_news


class TestSum(unittest.TestCase):

    def test_fetch_WHKS_news(self):
        news = []
        news = yahoo_news.get_news("WKHS")

        print(news)
        self.assertEqual("Benzinga", news.author)
        self.assertEqual("Shares of Workhorse Group (NASDAQ: WKHS) saw some unusual options activity on Friday. Following the unusual option alert, the stock price moved up to $21.95", news.text)


if __name__ == '__main__':
    unittest.main()