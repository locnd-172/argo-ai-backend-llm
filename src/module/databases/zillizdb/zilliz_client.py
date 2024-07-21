from pymilvus import MilvusClient

from src.config.constant import ZillizCFG
from src.module.llm.embedding.gemini_embedding import GeminiEmbeddingModel
from src.utils.logger import logger


class ZillizClient:
    def __init__(self, collection_name):
        self.uri = f'https://{ZillizCFG.ZILLIZDB_HOST}'
        self.token = ZillizCFG.ZILLIZDB_TOKEN
        self.collection_name = collection_name
        logger.info("index: %s", self.collection_name)
        self.client = self.connect_db()

    def connect_db(self):
        client = MilvusClient(
            uri=self.uri,
            token=self.token
        )
        return client

    def disconnect_db(self):
        self.client.close()

    def reset_db(self):
        self.client.drop_collection(self.collection_name)

    def insert_records(self, records):
        self.client.insert(self.collection_name, records)

    def get_all_records(self):
        return self.client.query(
            collection_name=self.collection_name,
            filter="",
            limit=100,
            output_fields=["id", "title", "language", "source"]
        )

    def get_all_documents(self, batch_size=200):
        all_documents = []
        offset = 0
        while True:
            try:
                documents = self.client.query(
                    collection_name=self.collection_name,
                    filter="",
                    limit=batch_size,
                    offset=offset,
                    output_fields=["id", "title", "language", "source", "status", "source_type", "created_at"]
                )
                if not documents:
                    break
                all_documents.extend(documents)
                offset += batch_size
            except Exception as e:
                logger.error("Error retrieving all documents: %s", str(e))
                break
        return all_documents

    def vector_search(self, query, limit_num=16):
        embedding = GeminiEmbeddingModel()
        query_emb = embedding.get_embedding(query, task_type="retrieval_query")
        query_emb = query_emb.get("embedding")
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_emb],
            limit=limit_num,
            search_params={
                "metric_type": "COSINE",
                "params": {}
            },
            output_fields=["id", "title", "content", "source"],
        )
        return results

    def delete_by_id(self, ids=None, filters=""):
        try:
            self.client.delete(
                collection_name=self.collection_name,
                ids=ids,
                filter=filters
            )
            return True
        except Exception as e:
            return False
