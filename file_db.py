from dotenv import load_dotenv

load_dotenv(override=True)


class FileDatabase:
    def __init__(self, file_name):
        self._file_name = file_name
        with open(file_name, 'r') as f:
            self._db = f.read().splitlines()
        self._list_of_stocks = list(self._db)

    def add_stock(self, stock_name):
        self._list_of_stocks.append(stock_name)
        self.write_list_to_file(self._list_of_stocks)
        self.read_file()

    def get_stocks(self):
        self.read_file()
        return self._list_of_stocks

    def remove_stock(self, stock_name):
        temp_list = list(self._list_of_stocks)
        for ticker in temp_list:
            if stock_name == ticker:
                self._list_of_stocks.remove(stock_name)
        self.write_list_to_file(self._list_of_stocks)
        self.read_file()

    def read_file(self):
        with open(self._file_name, 'r') as f:
            self._db = f.read().splitlines()
        self._list_of_stocks = list(self._db)

    def write_list_to_file(self, stock_list):
        with open(self._file_name, "w") as f:
            [f.write("{0}\n".format(stock))
             for stock in stock_list]
