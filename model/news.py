class StockInfo:
    def __init__(self, uuid, title, author, published_at, text, url, stock_name):
        self.uuid = uuid
        self.title = title
        self.author = author
        self.published_at = published_at
        self.text = text
        self.url = url
        self.stock_name = stock_name

    def __str__(self):
        return 'uuid= {self.uuid}\ntitle= {self.title}\nauthor= {self.author}\npublished_at= {self.published_at}\ntext= {self.text}\nurl= {self.url}\nstock_name= {self.stock_name}\n'.format(
            self=self)
