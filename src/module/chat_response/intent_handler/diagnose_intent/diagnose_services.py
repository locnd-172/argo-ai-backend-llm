from src.module.llm.gemini.gemini_services import call_model_gemini_multimodal
from src.module.llm.prompts.prompt_diagnose import PROMPT_DIAGNOSE
from src.utils.logger import logger


async def get_diagnose_response(data, file, language):
    formatted_prompt = PROMPT_DIAGNOSE.format(language=language)
    logger.info("DIAGNOSE PROMPT: %s", formatted_prompt)
    diagnose_info_resp = await call_model_gemini_multimodal(prompt=formatted_prompt, file=file)
    logger.info("DIAGNOSE INFO: %s", diagnose_info_resp)
    answer = diagnose_info_resp.get("response")
    return answer
