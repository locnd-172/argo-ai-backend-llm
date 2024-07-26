from typing import Dict, Any, List

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

from src.config.constant import FirebaseCFG

cred = credentials.Certificate(FirebaseCFG.FS_CERTIFICATE_PATH)
firebase_admin.initialize_app(cred)


class FirestoreWrapper:
    def __init__(self):
        self.db = firestore.client()

    async def insert_data(self, collection_name: str, data: Dict[str, Any], document_id=None) -> str:
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.set(data, merge=True)
        return doc_ref.id

    async def retrieve_data(
            self,
            collection_name: str,
            document_id: str = None,
            query_filters: List[tuple] = None,
            order_by: str = None
    ):
        collection_ref = self.db.collection(collection_name)

        if document_id:
            doc_ref = collection_ref.document(document_id)
            doc = doc_ref.get()
            return [{"id": doc_ref.id, **doc.to_dict()}] if doc.exists else []

        if query_filters:
            for field, operator, value in query_filters:
                collection_ref = collection_ref.where(filter=FieldFilter(field, operator, value))

        if order_by:
            collection_ref.order_by(order_by, ascending=False).limit(1)

        docs = collection_ref.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    async def update_document(
            self,
            collection_name: str,
            document_id: str,
            updated_data: Dict[str, Any]
    ):
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.update(updated_data)
        return doc_ref.id

    async def delete_document(self, collection_name: str, document_id: str):
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.delete()
            return True
        except Exception as e:
            return False
