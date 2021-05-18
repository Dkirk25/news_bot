import firebase_admin
from google.cloud import firestore
from dotenv import load_dotenv
load_dotenv(override=True)

class FirebaseDatabase:
    def __init__(self):
        firebase_admin.initialize_app()
        self._db = firestore.Client()

    def create_collection(self):
        self._db.collection(u'stocks')

    def add_stock(self,stock_name):
        doc_ref = self._db.collection(u'stocks').document(stock_name)
        doc_ref.set({
            u'name': stock_name,
        })

    def get_stocks(self):
        stocks_ref = self._db.collection(u'stocks')
        docs = stocks_ref.stream()

        list_of_stocks = []
        [list_of_stocks.append(doc.id) for doc in docs]
        return list_of_stocks

    def remove_stock(self, stock_name):
        self._db.collection(u'stocks').document(stock_name).delete()