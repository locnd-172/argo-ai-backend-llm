from src.config.constant import FirebaseCFG, QADocsCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.utils.logger import logger


async def get_chat_statistic():
    firestore = FirestoreWrapper()
    conversations = await firestore.retrieve_data(
        collection_name=FirebaseCFG.FS_COLLECTION_CONVERSATION,
    )
    total_conversations = len(conversations)
    logger.info("conversations: {}".format(conversations))
    intent_counts, qna_intent_counts = aggregate_chat_statistic(conversations)
    return {
        "total_conversations": total_conversations,
        "intent_counts": intent_counts,
        "qna_intent_counts": qna_intent_counts,
    }


def aggregate_chat_statistic(conversations):
    intent_counts = {}
    qna_intent_counts = {}
    for item in conversations:
        intent_value = item['intent']
        qna_intent_value = item['qna_intent']
        intent_counts[intent_value] = intent_counts.get(intent_value, 0) + 1
        qna_intent_key = qna_intent_value if qna_intent_value in QADocsCFG.INTENTS else "other"
        qna_intent_counts[qna_intent_key] = qna_intent_counts.get(qna_intent_key, 0) + 1

    return intent_counts, qna_intent_counts
