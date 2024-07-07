from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_recommend import (
    PROMPT_EXTRACT_RECOMMEND_INFO, PROMPT_RECOMMEND)
from src.utils.logger import logger


def extract_recommendation_info(data):
    formatted_prompt = PROMPT_EXTRACT_RECOMMEND_INFO.format(message=data.sender_message)
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
    formatted_prompt = PROMPT_RECOMMEND.format(
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


def get_recommend_response(data, language, histories):
    recom_info = extract_recommendation_info(data)
    recom_resp = get_recommendation(inputs=recom_info, language=language, histories=histories)
    answer = recom_resp.get("response")
    return answer
