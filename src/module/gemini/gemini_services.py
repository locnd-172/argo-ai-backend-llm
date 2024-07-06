from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from src.config.constant import GeminiAiCFG
from src.module.gemini.gemini_client import GeminiAI


@retry(stop=(stop_after_delay(30) | stop_after_attempt(3)), wait=wait_fixed(1))
def call_model_gemini(prompt):
    try:
        gemini_client = GeminiAI(
            api_key=GeminiAiCFG.API_KEY,
            api_model=GeminiAiCFG.API_MODEL
        )
        generated_content = gemini_client.generate_content_json(prompt)
        return generated_content
    except Exception as e:
        raise e


@retry(stop=(stop_after_delay(30) | stop_after_attempt(3)), wait=wait_fixed(1))
async def call_model_gemini_multimodal(prompt, file):
    try:
        image_data = None
        if file:
            image_content = await file.read()
            image_data = {
                "data": image_content,
                "mime_type": file.content_type,
            }

        gemini_client = GeminiAI(
            api_key=GeminiAiCFG.API_KEY,
            api_model=GeminiAiCFG.API_MODEL
        )
        generated_content = gemini_client.generate_content_json(prompt=prompt, img=image_data)
        return generated_content
    except Exception as e:
        raise e
