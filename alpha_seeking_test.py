from model.news import StockInfo
import unittest
import alpha_seeking


class TestSum(unittest.TestCase):

    def test_fetch_WHKS_news(self):
        news = []
        news = alpha_seeking.get_news("WKHS")

        print(news)
        self.assertEqual("Workhorse -9% with USPS said to delaying big contract decision", news)


if __name__ == '__main__':
    unittest.main()