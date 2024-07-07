from src.config.constant import IntentCFG, LanguageCFG, AppMessages
from src.module.chat_response.intent_detection.intent_services import get_intent_info
from src.module.chat_response.intent_handler import (get_diagnose_response,
                                                     get_docs_qa_response,
                                                     get_generic_response,
                                                     get_recommend_response,
                                                     get_report_response)
from src.utils.logger import logger


async def generate_chat_response(data, file, histories):
    logger.info("HISTORIES: %s", histories)

    intent_info = get_intent_info(data) or {}

    intent = intent_info.get(IntentCFG.INTENT, IntentCFG.GENERIC)
    language = intent_info.get(IntentCFG.LANGUAGE, LanguageCFG.EN)

    answer = "No answer"
    if intent == IntentCFG.GENERIC:
        answer = get_generic_response(data=data, language=language)
    elif intent == IntentCFG.QNA:
        answer = get_docs_qa_response(data=data, language=language)
    elif intent == IntentCFG.REPORT:
        answer = get_report_response(data=data, language=language)
    elif intent == IntentCFG.RECOMMENDATION:
        answer = get_recommend_response(data=data, language=language, histories=histories)
    elif intent == IntentCFG.DIAGNOSE:
        answer = await get_diagnose_response(data=data, language=language, file=file)
    elif intent == IntentCFG.SENSITIVE:
        answer = get_sensitive_response(language=language)

    chat_response = {"response": answer}
    return chat_response


def get_sensitive_response(language):
    language = language.lower() or "vietnam"
    message_by_language = AppMessages.SENSITIVE_MSG.get(language)
    return message_by_language
