import unittest
from yahoo_news import YahooHelper
from discord_helper import DiscordHelper
from pytz import timezone, all_timezones
from datetime import date, timedelta, datetime
from pytz import timezone


class TestSum(unittest.TestCase):

    def test_validate_timestamp(self):
        yahoo_news = YahooHelper()
        discord_helper = DiscordHelper()

        news = []
        news = yahoo_news.fetch_news("mro")[0]

        # check if date is from last 5 days
        nice_date = discord_helper.get_clean_date(news.published_at)

        central_timezone = timezone('US/Central')

        stock_date = nice_date.strftime(
            '%B %d, %Y, %I:%M %p')

        # self.assertTrue(datetime.now()-timedelta(5) <= nice_date)

        # April 23, 2021, 2:12 PM
        self.assertEqual("April 23, 2021, 02:12 PM", str(stock_date))

        # self.assertTrue(discord_helper.is_newer_date(
        #     discord_helper.get_clean_date(news.published_at)))

        # discord shows Today at 9:21 AM


if __name__ == '__main__':
    unittest.main()
