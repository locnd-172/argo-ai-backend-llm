import json

from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from src.config.constant import GeminiAiCFG
from src.module.gemini.gemini_client import GeminiAI
from src.module.gemini.prompts import PROMPT_GENERATE_EVENT_CONTENT
from src.utils.logger import logger


@retry(stop=(stop_after_delay(30) | stop_after_attempt(3)), wait=wait_fixed(1))
def call_model_gen_content(prompt):
    logger.info("GENERATE EVENT CONTENT PROMPT:\n%s", prompt)
    try:
        gemini_client = GeminiAI(
            api_key=GeminiAiCFG.API_KEY,
            api_model=GeminiAiCFG.API_MODEL
        )
        generated_content = gemini_client.generate_content_json(prompt)
        return generated_content
    except Exception as e:
        raise e


def generate_event_content(event_data):
    formatted_prompt = PROMPT_GENERATE_EVENT_CONTENT.format(
        event_name=event_data.event_name,
        event_format=event_data.event_format,
        event_categories=event_data.event_categories,
        event_description=event_data.event_description,
        event_detail_info=event_data.event_detail_info
    )

    generated_content = call_model_gen_content(formatted_prompt)

    logger.info(
        "GENERATED EVENT CONTENT: %s", str(json.dumps(
            generated_content, indent=4, ensure_ascii=False))
    )
    return generated_content
