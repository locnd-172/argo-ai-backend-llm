import json

from src.config.constant import AppMessages, IntentCFG, LanguageCFG
from src.module.chat_response.intent_detection.intent_services import get_intent_info
from src.module.chat_response.intent_handler import (
    get_diagnose_response,
    get_docs_qa_response,
    get_generic_response,
    get_recommend_response,
    get_report_response
)
from src.utils.logger import logger


async def generate_chat_response(data, file, histories):
    logger.info("HISTORIES: %s", histories)

    intent_info = get_intent_info(data, histories) or {}

    intent = intent_info.get(IntentCFG.INTENT, IntentCFG.GENERIC)
    language = intent_info.get(IntentCFG.LANGUAGE, LanguageCFG.EN)
    standalone_query = intent_info.get(IntentCFG.STANDALONE_QUERY, data.sender_message)

    answer = "No answer"
    follow_ups = []
    chat_response = {"response": answer, "follow_ups": follow_ups}

    if intent == IntentCFG.SENSITIVE:
        chat_response = get_sensitive_response(language=language)
    elif intent == IntentCFG.REPORT:
        chat_response = get_report_response(data=data, language=language)
    elif intent == IntentCFG.GENERIC:
        chat_response = get_generic_response(data=data, language=language)
    elif intent == IntentCFG.DIAGNOSE:
        chat_response = await get_diagnose_response(
            data=data,
            language=language,
            file=file
        )
    elif intent == IntentCFG.RECOMMENDATION:
        chat_response = get_recommend_response(
            data=data,
            language=language,
            standalone_query=standalone_query,
            histories=histories,
        )
    elif intent == IntentCFG.QNA:
        chat_response = get_docs_qa_response(
            data=data,
            language=language,
            standalone_query=standalone_query,
            histories=histories,
        )

    logger.info("CHAT RESPONSE: %s", json.dumps(chat_response, indent=4, ensure_ascii=False))
    return chat_response


def get_sensitive_response(language):
    language = language.lower() or "vietnam"
    message_by_language = AppMessages.SENSITIVE_MSG.get(language)
    return {"response": message_by_language, "follow_ups": []}
