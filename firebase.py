import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.RefreshToken('./argoai-63051-firebase-adminsdk-ykwbi-a14bbb8c68.json')

app = firebase_admin.initialize_app()
db = firestore.client()

batch = db.batch()

# Set the data for NYC
nyc_ref = db.collection("cities").document("NYC")
batch.set(nyc_ref, {"name": "New York City"})