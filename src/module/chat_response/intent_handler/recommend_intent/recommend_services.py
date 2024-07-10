from src.module.chat_response.intent_handler.docs_qa_intent.docs_helpers import get_conversation_histories
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_recommend import PROMPT_EXTRACT_RECOMMEND_INFO, PROMPT_RECOMMEND
from src.utils.logger import logger


async def extract_recommendation_info(data, standalone_query):
    message = standalone_query if standalone_query else data.sender_message
    formatted_prompt = PROMPT_EXTRACT_RECOMMEND_INFO.format(message=message)
    logger.info("PROMPT EXTRACT RECOMMEND INFO: {}".format(formatted_prompt))

    recommendation_info_resp = await call_model_gemini(formatted_prompt)
    logger.info("RECOMMENDATION INFO: %s", recommendation_info_resp)

    return recommendation_info_resp


async def get_recommendation(inputs, language, histories):
    conv_str = get_conversation_histories(histories)
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

    recommendation_resp = await call_model_gemini(formatted_prompt)
    logger.info("RECOMMENDATION RESPONSE: %s", recommendation_resp)

    return recommendation_resp


async def get_recommend_response(chat_request):
    data = chat_request.data
    recom_info = await extract_recommendation_info(data, chat_request.standalone_query)
    recom_resp = await get_recommendation(
        inputs=recom_info,
        language=chat_request.language,
        histories=chat_request.histories
    )
    return recom_resp
