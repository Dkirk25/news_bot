import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import os
from dotenv import load_dotenv
load_dotenv(override=True)

class FirebaseDatabase:
    def __init__(self):
        self._cred =credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(self._cred)
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