import json

from src.config.constant import AppMessages, IntentCFG, LanguageCFG
from src.models.chat_model import GenerationRequest
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

    intent_info = await get_intent_info(data, histories) or {}

    intent = intent_info.get(IntentCFG.INTENT, IntentCFG.GENERIC)
    language = intent_info.get(IntentCFG.LANGUAGE, LanguageCFG.EN)
    standalone_query = intent_info.get(IntentCFG.STANDALONE_QUERY, data.sender_message)

    chat_request = GenerationRequest(
        data=data,
        file=file,
        histories=histories,
        language=language,
        standalone_query=standalone_query
    )
    chat_response = {"response": "No answer", "follow_up": []}

    response_func_map = {
        IntentCFG.QNA: get_docs_qa_response,
        IntentCFG.REPORT: get_report_response,
        IntentCFG.GENERIC: get_generic_response,
        IntentCFG.DIAGNOSE: get_diagnose_response,
        IntentCFG.SENSITIVE: get_sensitive_response,
        IntentCFG.RECOMMENDATION: get_recommend_response,
    }

    if intent in response_func_map:
        response_func = response_func_map[intent]
        chat_response = await response_func(chat_request)

    chat_response["intent"] = intent
    logger.info("CHAT RESPONSE: %s", json.dumps(chat_response, indent=4, ensure_ascii=False))
    return chat_response


async def get_sensitive_response(chat_request):
    language = chat_request.language
    language = language.lower() or "vietnam"
    message_by_language = AppMessages.SENSITIVE_MSG.get(language)
    return {"response": message_by_language, "follow_up": []}
