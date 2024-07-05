import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./argoai-63051-firebase-adminsdk-ykwbi-a14bbb8c68.json')

app = firebase_admin.initialize_app(cred)
db = firestore.client()