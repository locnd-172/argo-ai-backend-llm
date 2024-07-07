from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_generic import PROMPT_GENERIC
from src.utils.helpers import get_current_datetime
from src.utils.logger import logger


def get_generic_response(data, language):
    formatted_prompt = PROMPT_GENERIC.format(
        message=data.sender_message,
        language=language,
        now=get_current_datetime()
    )
    generic_response = call_model_gemini(formatted_prompt)
    logger.info("GENERIC ANSWER: %s", generic_response)
    generic_answer = generic_response.get("response")
    return generic_answer
