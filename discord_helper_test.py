import unittest
from yahoo_news import YahooHelper
from discord_helper import DiscordHelper
from pytz import timezone
from datetime import date, timedelta, datetime
from pytz import timezone


class TestSum(unittest.TestCase):

    def test_validate_timestamp(self):
        yahoo_news = YahooHelper()
        discord_helper = DiscordHelper()

        news = []
        news = yahoo_news.fetch_news("xela")[0]

        # check if date is from last 5 days
        nice_date = discord_helper.get_clean_date(news.published_at)

        self.assertTrue(datetime.now()-timedelta(5) <= nice_date)

        # self.assertEqual("April 21, 2021, 7:30 AM", news.published_at)

        # discord shows Today at 9:21 AM


if __name__ == '__main__':
    unittest.main()
