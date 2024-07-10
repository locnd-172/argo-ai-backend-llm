import json

import google.generativeai as genai


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

    async def generate_content(self, prompt: str):
        response = await self.model.generate_content_async(prompt)
        return response

    async def generate_content_multimodal(self, prompt: str, image):
        response = await self.model.generate_content_async([prompt, image])
        return response

    async def generate_content_json(self, prompt: str, img=None):
        if img is not None:
            response = await self.generate_content_multimodal(prompt=prompt, image=img)
        else:
            response = await self.generate_content(prompt=prompt)

        response_text = post_process_json_string(response.text)
        response_json = json.loads(response_text, strict=False)
        return response_json
