import unittest

from yahoo_news_2 import YahooHelper2

from discord_helper import DiscordHelper


class TestSum(unittest.TestCase):

    def test_validate_timestamp(self):
        yahoo_news = YahooHelper2()
        discord_helper = DiscordHelper()

        news = []
        news = yahoo_news.fetch_news("f")[0]

        # check if date is from last 5 days
        # nice_date = discord_helper.get_clean_date(news.published_at)

        nice_date = discord_helper.embed_date(news.published_at)

        # stock_date = nice_date.strftime(
        #     '%B %d, %Y, %I:%M %p')

        # April 23, 2021, 2:12 PM
        self.assertEqual("April 27, 2021, 11:04 AM", nice_date)

        # self.assertTrue(discord_helper.is_newer_date(
        #     discord_helper.get_clean_date(news.published_at)))

        # discord shows Today at 9:21 AM


if __name__ == '__main__':
    unittest.main()
