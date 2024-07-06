import json

from src.config.constant import IntentCFG, LanguageCFG
from src.module.gemini.gemini_services import call_model_gemini, call_model_gemini_multimodal
from src.module.gemini.prompts import (
    PROMPT_INTENT_DETECTION,
    PROMPT_GENERIC,
    PROMPT_EXTRACT_RECOMMENDATION_INFO,
    PROMPT_RECOMMENDATION,
    PROMPT_EXTRACT_REPORT_INFO, PROMPT_DIAGNOSE
)
from src.module.report_intent import report_services
from src.utils.helpers import get_current_datetime
from src.utils.logger import logger


async def generate_chat_response(data, file, histories):
    intent_info = get_intent_info(data) or {}

    logger.info("HISTORIES: %s", histories)
    # logger.info("intent_info: %s", intent_info)
    intent = intent_info.get(IntentCFG.INTENT, IntentCFG.GENERIC)
    language = intent_info.get(IntentCFG.LANGUAGE, LanguageCFG.EN)

    answer = "No answer"
    if intent == IntentCFG.GENERIC:
        answer = get_generic_answer(data, language)
    elif intent == IntentCFG.QNA:
        # answer = "qna"
        answer = get_generic_answer(data, language)
    elif intent == IntentCFG.REPORT:
        answer = get_report_response(data, language)
    elif intent == IntentCFG.DIAGNOSE:
        answer = await get_diagnose_response(data=data, file=file, language=language)
    elif intent == IntentCFG.RECOMMENDATION:
        recom_info = extract_recommendation_info(data)
        recom_resp = get_recommendation(inputs=recom_info, language=language, histories=histories)
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
        language=language,
        now=get_current_datetime()
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


def get_recommendation(inputs, language, histories):
    last_conv = histories[-1] if len(histories) > 1 else []
    conv_str = ""
    if len(last_conv) > 0:
        conv_str = f"""user: {last_conv['user']}
bot: {last_conv['bot']}
"""

    formatted_prompt = PROMPT_RECOMMENDATION.format(
        facility=inputs.get("facility", "unknown"),
        location=inputs.get("location", "Vietnam"),
        plant=inputs.get("plant", ""),
        period=inputs.get("period", "this month"),
        status=inputs.get("status", "unknown"),
        metrics=inputs.get("metrics", "general"),
        language=language,
        history=conv_str
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


def get_report_response(data, language):
    report_info = extract_report_info(data)
    report_data = report_services.query_report_data(report_info)
    report_resp = report_services.gen_report_answer(
        report_data=report_data,
        language=language,
        report_info=report_info
    )
    answer = report_resp.get("response")
    return answer


def get_response_docs_qn(data):
    ...


async def get_diagnose_response(data, file, language):
    formatted_prompt = PROMPT_DIAGNOSE.format(language=language)
    logger.info("DIAGNOSE PROMPT: %s", formatted_prompt)
    diagnose_info_resp = await call_model_gemini_multimodal(prompt=formatted_prompt, file=file)
    logger.info("DIAGNOSE INFO: %s", diagnose_info_resp)
    answer = diagnose_info_resp.get("response")
    return answer
