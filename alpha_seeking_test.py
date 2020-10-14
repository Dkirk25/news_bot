from model.news import StockInfo
import unittest
import alpha_seeking


class TestSum(unittest.TestCase):

    def test_fetch_WHKS_news(self):
        news = alpha_seeking.get_news("WKHS")

        print(news)
        self.assertEqual("WKHS downgraded by Roth Capital analyst", news["title"])


if __name__ == '__main__':
    unittest.main()