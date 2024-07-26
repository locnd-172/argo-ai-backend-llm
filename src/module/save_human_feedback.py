import json
import time
import traceback
import uuid

from src.config.constant import ZillizCFG
from src.module.databases.zillizdb.zilliz_client import ZillizClient
from src.module.llm.embedding.gemini_embedding import GeminiEmbeddingModel
from src.utils.logger import logger


async def save_human_feedback(data):
    embedding_model = GeminiEmbeddingModel()
    embedding = embedding_model.get_embedding(
        text=data.sender_message,
        task_type="retrieval_document",
        title="document"
    )
    feedback = {
        "id": str(uuid.uuid4()),
        "vector": embedding.get("embedding"),
        "query": str(data.sender_message),
        "answer": str(data.response_message),
        "feedback": str(data.human_feedback),
        "created_at": time.time(),
    }
    insert_result = insert_feedback_to_zilliz([feedback])
    logger.info("insert_result: %s", insert_result)
    return {"result": insert_result}


def insert_feedback_to_zilliz(documents):
    filtered_item = [{key: value for key, value in item.items() if key != 'vector'} for item in documents]
    logger.info("filtered_item: %s", json.dumps(filtered_item, indent=4, ensure_ascii=False))
    try:
        zilliz = ZillizClient(ZillizCFG.ZILLIZDB_COLLECTION_NAME_HUMAN_FEEDBACKS)
        zilliz.insert_records(documents)
        return True
    except Exception as e:
        logger.error(e, traceback.format_exc())
        return False
