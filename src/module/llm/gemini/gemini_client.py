import json

import google.generativeai as genai

from src.utils.logger import logger


def post_process_json_string(text: str):
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()
    return text


class GeminiAI:

    def __init__(self, api_key, api_model):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=api_model,
            generation_config={"response_mime_type": "application/json"}
        )

    async def generate_content(self, prompt: str, stream: bool):
        response = await self.model.generate_content_async(prompt, stream=stream)
        return response

    async def generate_content_multimodal(self, prompt: str, image, stream: bool):
        response = await self.model.generate_content_async([prompt, image], stream=stream)
        return response

    async def generate_content_json(self, prompt: str, img=None, stream=False):
        if img is not None:
            response = self.generate_content_multimodal(prompt=prompt, image=img, stream=stream)
        else:
            response = await self.generate_content(prompt=prompt, stream=stream)
        await response.resolve()
        response_text = post_process_json_string(response.text)
        response_json = json.loads(response_text, strict=False)
        logger.info("Response text:\n%s", response_json)
        return response_json

    async def generate_content_json_stream(self, prompt: str, img=None, ):
        if img is not None:
            response = self.generate_content_multimodal(prompt=prompt, image=img, stream=True)
        else:
            response = await self.generate_content(prompt=prompt, stream=True)
        logger.info("Response: %s", response)
        async for chunk in response:
            chunk_decoded = chunk.text
            yield f"{chunk_decoded}"
