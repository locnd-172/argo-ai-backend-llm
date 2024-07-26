import json
import time
import traceback
import uuid

from src.config.constant import ZillizCFG, FirebaseCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
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
        "message_id": str(data.message_id),
        "vector": embedding.get("embedding"),
        "query": str(data.sender_message),
        "answer": str(data.response_message),
        "feedback": str(data.human_feedback),
        "created_at": time.time(),
    }
    insert_result = insert_feedback_to_zilliz([feedback])
    await add_feedback_to_conversation(data=data, human_feedback=str(data.human_feedback))
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


async def add_feedback_to_conversation(data, human_feedback):
    firestore = FirestoreWrapper()
    conversations = await firestore.retrieve_data(
        collection_name=FirebaseCFG.FS_COLLECTION_CONVERSATION,
        query_filters=[("message_id", "==", data.message_id)]
    )
    conversation = {}
    if len(conversations) > 0:
        conversation = conversations[0]
    if conversation:
        conversation["feedback"] = human_feedback
        logger.info("UPSERT CONVERSATION: %s", conversation)
        insert_result = await firestore.insert_data(
            collection_name=FirebaseCFG.FS_COLLECTION_CONVERSATION,
            data=conversation,
            document_id=conversation.get("id", None)
        )
        logger.info("UPDATE CONVERSATION RESULT: %s", insert_result)
