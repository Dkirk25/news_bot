class StockInfo:
    def __init__(self, uuid, title, author, published_at, text, url):
        self.uuid = uuid
        self.title = title
        self.author = author
        self.published_at = published_at
        self.text = text
        self.url = url

    def __str__(self):
        return 'uuid= {self.uuid}\ntitle= {self.title}\nauthor= {self.author}\npublished_at= {self.published_at}\ntext= {self.text}\nurl= {self.url}\n'.format(
            self=self)
