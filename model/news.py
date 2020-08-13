class StockInfo:
    def __init__(self, title, author, text, url):
        self.title = title
        self.author = author
        self.text = text
        self.url = url

    def __str__(self):
        return 'title= {self.title}\nauthor= {self.author}\ntext= {self.text}\nurl= {self.url}\n'.format(
            self=self)
