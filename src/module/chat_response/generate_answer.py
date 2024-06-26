import json

from src.config.constant import IntentCFG, LanguageCFG
from src.module.gemini.gemini_services import call_model_gemini
from src.module.gemini.prompts import (
    PROMPT_INTENT_DETECTION,
    PROMPT_GENERIC,
    PROMPT_EXTRACT_RECOMMENDATION_INFO,
    PROMPT_RECOMMENDATION, PROMPT_EXTRACT_REPORT_INFO
)
from src.utils.logger import logger


def generate_chat_response(data):
    intent_info = get_intent_info(data) or {}

    logger.info("intent_info: %s", intent_info)
    intent = intent_info.get(IntentCFG.INTENT, IntentCFG.GENERIC)
    language = intent_info.get(IntentCFG.LANGUAGE, LanguageCFG.EN)

    answer = "No answer"
    if intent == IntentCFG.GENERIC:
        answer = get_generic_answer(data, language)
    elif intent == IntentCFG.QNA:
        answer = "qna"
    elif intent == IntentCFG.REPORT:
        answer = "report"
        report_info = extract_recommendation_info(data)
        report_resp = get_recommendation(inputs=report_info)
        answer = report_resp.get("response")
    elif intent == IntentCFG.RECOMMENDATION:
        answer = "recommendation"
        # answer = get_generic_answer(data, language)
        recom_info = extract_recommendation_info(data)
        recom_resp = get_recommendation(inputs=recom_info)
        answer = recom_resp.get("response")
    elif intent == IntentCFG.SENSITIVE:
        answer = "sensitive"

    chat_response = {
        "response": answer
    }
    return chat_response


def get_intent_info(data):
    formatted_prompt = PROMPT_INTENT_DETECTION.format(message=data.sender_message)
    intent_info_resp = call_model_gemini(formatted_prompt)
    logger.info("INTENT INFO: %s", json.dumps(intent_info_resp, indent=4, ensure_ascii=False))
    return intent_info_resp


def get_generic_answer(data, language):
    formatted_prompt = PROMPT_GENERIC.format(
        message=data.sender_message,
        language=language
    )
    generic_response = call_model_gemini(formatted_prompt)
    logger.info("GENERIC ANSWER: %s", generic_response)
    generic_answer = generic_response.get("response")
    return generic_answer


def extract_recommendation_info(data):
    formatted_prompt = PROMPT_EXTRACT_RECOMMENDATION_INFO.format(message=data.sender_message)
    recommendation_info_resp = call_model_gemini(formatted_prompt)
    logger.info("RECOMMENDATION INFO: %s", recommendation_info_resp)
    return recommendation_info_resp


def get_recommendation(inputs):
    formatted_prompt = PROMPT_RECOMMENDATION.format(
        facility=inputs.get("facility", "unkonwn"),
        location=inputs.get("location", "Vietnam"),
        plant=inputs.get("plant", ""),
        period=inputs.get("period", "this month"),
        status=inputs.get("status", "unknown"),
        metrics=inputs.get("metrics", "general planting"),
    )
    logger.info("RECOMMENDATION PROMPT:\n%s", formatted_prompt)
    recommendation_resp = call_model_gemini(formatted_prompt)
    logger.info("RECOMMENDATION RESPONSE: %s", recommendation_resp)
    return recommendation_resp


def extract_report_info(data):
    formatted_prompt = PROMPT_EXTRACT_REPORT_INFO.format(message=data.sender_message)
    report_info_resp = call_model_gemini(formatted_prompt)
    logger.info("REPORT INFO: %s", report_info_resp)
    return report_info_resp
