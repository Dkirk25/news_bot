import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('./news-bot-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def create_collection():
    doc_ref = db.collection(u'stocks').document(u'WKHS')
    doc_ref.set({
        u'name': u'WKHS',
    })


def add_stock(stock_name):
    doc_ref = db.collection(u'stocks').document(stock_name)
    doc_ref.set({
        u'name': stock_name,
    })


def get_stocks():
    stocks_ref = db.collection(u'stocks')
    docs = stocks_ref.stream()

    list_of_stocks = []
    for doc in docs:
        list_of_stocks.append(doc.id)
    return list_of_stocks


def remove_stock(stock_name):
    db.collection(u'stocks').document(stock_name).delete()
