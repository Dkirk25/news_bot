import unittest
from file_db import FileDatabase


class TestSum(unittest.TestCase):

    def test_get_tickers(self):
        file_db = FileDatabase("full_ticker.txt")

        expected = file_db.get_stocks()

        self.assertEqual("ARKQ", expected[0])

    def test_add_tickers(self):
        added_stocks = ["BBW", "abc", "cool"]
        file_db = FileDatabase("full_ticker.txt")

        for stock in added_stocks:
            file_db.add_stock(stock)

        list_of_stocks = file_db.get_stocks()

        self.assertTrue(
            all(stocks in list_of_stocks for stocks in added_stocks))

    def test_remove_tickers(self):
        remove_stocks = ["BBW", "abc", "cool"]
        file_db = FileDatabase("full_ticker.txt")

        for stock in remove_stocks:
            file_db.remove_stock(stock)

        list_of_stocks = file_db.get_stocks()

        self.assertFalse(
            all(stocks in list_of_stocks for stocks in remove_stocks))


if __name__ == '__main__':
    unittest.main()
