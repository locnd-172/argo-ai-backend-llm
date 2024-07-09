from src.module.llm.gemini.gemini_services import call_model_gemini_multimodal
from src.module.llm.prompts.prompt_diagnose import PROMPT_DIAGNOSE
from src.utils.logger import logger


async def get_diagnose_response(chat_request):
    formatted_prompt = PROMPT_DIAGNOSE.format(language=chat_request.language)
    logger.info("DIAGNOSE PROMPT: %s", formatted_prompt)
    diagnose_info_resp = await call_model_gemini_multimodal(
        prompt=formatted_prompt,
        file=chat_request.file
    )
    logger.info("DIAGNOSE INFO: %s", diagnose_info_resp)
    return diagnose_info_resp
