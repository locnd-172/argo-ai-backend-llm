from src.config.constant import FirebaseCFG, QADocsCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.utils.logger import logger

from src.module.llm.prompts.prompt_qna_analytic import PROMPT_QNA_ANALYTIC
async def get_chat_statistic():
    firestore = FirestoreWrapper()
    conversations = await firestore.retrieve_data(
        collection_name=FirebaseCFG.FS_COLLECTION_CONVERSATION,
    )
    total_conversations = len(conversations)
    logger.info("conversations: {}".format(conversations))
    intent_counts, qna_intent_counts = aggregate_chat_statistic(conversations)
    insights = await analyze_chat_statistic(total_conversations, intent_counts, qna_intent_counts)

    return {
        "total_conversations": total_conversations,
        "intent_counts": intent_counts,
        "qna_intent_counts": qna_intent_counts,
        "insight": insights
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

async def analyze_chat_statistic(total_conversations, intent_counts, qna_intent_counts):
    formatted_prompt = PROMPT_QNA_ANALYTIC.format(
        total_conversations=total_conversations,
        qna=intent_counts.get('qna', ''),
        generic=intent_counts.get('generic', ''),
        agricultural_standards=qna_intent_counts.get('agricultural_standards', ''),
        cultivation_techniques=qna_intent_counts.get('cultivation_techniques', ''),
        other=qna_intent_counts.get('other', ''),
        general_agriculture=qna_intent_counts.get('general_agriculture', '')
    )
    logger.info("ANALYTIC QNA EMISSION: {}".format(formatted_prompt))

    qna_analytic_resp = await call_model_gemini(formatted_prompt)
    logger.info("GHG EMISSION RESULT: %s", qna_analytic_resp)
    return qna_analytic_resp
