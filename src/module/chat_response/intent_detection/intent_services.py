import json

from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_router import PROMPT_INTENT_DETECTION
from src.utils.logger import logger


def get_intent_info(data):
    formatted_prompt = PROMPT_INTENT_DETECTION.format(message=data.sender_message)
    intent_info_resp = call_model_gemini(formatted_prompt)
    logger.info("INTENT INFO: %s", json.dumps(intent_info_resp, indent=4, ensure_ascii=False))
    return intent_info_resp
