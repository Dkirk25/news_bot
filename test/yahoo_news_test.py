import unittest

from yahoo_news_2 import YahooHelper2


class TestSum(unittest.TestCase):

    # def test_fetch_WHKS_news(self):
    #     yahoo_news = YahooHelper()
    #     news = yahoo_news.fetch_news("SNDL")
    #     # Cf

    #     print(news)
    #     print(str(news[0]))
    #     # self.assertEqual("Benzinga", news.author)
    #     # self.assertEqual("Shares of Workhorse Group (NASDAQ: WKHS) saw some unusual options activity on Friday. Following the unusual option alert, the stock price moved up to $21.95", news.text)

    def test_fetch_WHKS_news(self):
        yahoo_news = YahooHelper2()
        news = yahoo_news.fetch_news("WKHS")
        # Cf

        print(news)
        print(str(news[0]))
        # self.assertEqual("Benzinga", news.author)
        # self.assertEqual("Shares of Workhorse Group (NASDAQ: WKHS) saw some unusual options activity on Friday. Following the unusual option alert, the stock price moved up to $21.95", news.text)

    # def test_fetch_WHKS_news(self):
    #     current_timestamp = datetime.timestamp()
    #     string_datetime = datetime.strftime(
    #         current_timestamp, '%B %d, %Y, %I:%M %p')

    # 'June 6, 2021, 7:20 AM'
    #     print(string_datetime)
    #     # self.assertEqual("Benzinga", news.author)
    # self.assertEqual("Shares of Workhorse Group (NASDAQ: WKHS) saw some unusual options activity on Friday. Following the unusual option alert, the stock price moved up to $21.95", news.text)


if __name__ == '__main__':
    unittest.main()
