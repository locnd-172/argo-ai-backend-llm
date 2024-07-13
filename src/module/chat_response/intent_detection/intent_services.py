import json

from src.module.chat_response.intent_handler.docs_qa_intent.docs_helpers import get_conversation_histories
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_router import PROMPT_INTENT_DETECTION
from src.utils.logger import logger


async def get_intent_info(data, histories):
    conv_str = get_conversation_histories(histories)
    formatted_prompt = PROMPT_INTENT_DETECTION.format(message=data.sender_message, histories=conv_str)

    intent_info_resp = await call_model_gemini(formatted_prompt, stream=False)
    logger.info("INTENT INFO: %s", intent_info_resp)
    # logger.info("INTENT INFO: %s", json.dumps(intent_info_resp, indent=4, ensure_ascii=False))

    return intent_info_resp
