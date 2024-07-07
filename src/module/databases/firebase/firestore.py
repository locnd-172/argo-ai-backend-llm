import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('argoai-63051-firebase-adminsdk-ykwbi-dd2916cb00.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
