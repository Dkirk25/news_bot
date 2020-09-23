import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# Use a service account
cred = credentials.Certificate(os.getenv("FIREBASE_KEY"))
firebase_admin.initialize_app(cred)

db = firestore.client()


def create_collection():
    db.collection(u'stocks')


def add_stock(stock_name):
    doc_ref = db.collection(u'stocks').document(stock_name)
    doc_ref.set({
        u'name': stock_name,
    })


def get_stocks():
    stocks_ref = db.collection(u'stocks')
    docs = stocks_ref.stream()

    list_of_stocks = []
    [list_of_stocks.append(doc.id) for doc in docs]
    return list_of_stocks


def remove_stock(stock_name):
    db.collection(u'stocks').document(stock_name).delete()
