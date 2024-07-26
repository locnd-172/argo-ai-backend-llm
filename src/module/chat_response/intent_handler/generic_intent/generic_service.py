from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_generic import PROMPT_GENERIC
from src.utils.helpers import get_current_datetime
from src.utils.logger import logger


async def get_generic_response(chat_request):
    data = chat_request.data
    formatted_prompt = PROMPT_GENERIC.format(
        message=data.sender_message,
        language=chat_request.language,
        now=get_current_datetime(),
        feedback_guide="",
        feedbacks=""
    )
    logger.info("GENERIC PROMPT: %s", formatted_prompt)
    generic_response = await call_model_gemini(formatted_prompt)
    generic_response["follow_up"] = []
    logger.info("GENERIC ANSWER: %s", generic_response)
    return generic_response
