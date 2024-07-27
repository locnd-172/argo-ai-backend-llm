import time
import uuid

from src.config.constant import FirebaseCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.utils.logger import logger


async def save_conversation(input_data, output_data):
    conversation = {
        "message_id": input_data.message_id,
        "created_time": time.time(),
        "session_id": input_data.session_id,
        "sender_id": input_data.sender_id,
        "sender_name": input_data.sender_name,
        "sender_message": input_data.sender_message,
        "response_message": output_data.get("response", ""),
        "intent": output_data.get("intent", "generic"),
        "qna_intent": output_data.get("qna_intent", None),
        "feedback": ""
    }
    logger.info("SAVING CONVERSATION: %s", conversation)
    firestore = FirestoreWrapper()
    insert_result = await firestore.insert_data(
        collection_name=FirebaseCFG.FS_COLLECTION_CONVERSATION,
        data=conversation,
    )
    logger.info("INSERT RESULT: %s", insert_result)
