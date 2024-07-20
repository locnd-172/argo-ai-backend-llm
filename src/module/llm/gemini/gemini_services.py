from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from src.config.constant import GeminiAiCFG
from src.module.llm.gemini.gemini_client import GeminiAI
from src.utils.logger import logger


@retry(stop=(stop_after_delay(30) | stop_after_attempt(3)), wait=wait_fixed(1))
async def call_model_gemini(prompt):
    try:
        gemini_client = GeminiAI(
            api_key=GeminiAiCFG.API_KEY,
            api_model=GeminiAiCFG.API_MODEL
        )
        generated_content = await gemini_client.generate_content_json(prompt)
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
        generated_content = await gemini_client.generate_content_json(prompt=prompt, img=image_data)
        return generated_content
    except Exception as e:
        raise e


@retry(stop=(stop_after_delay(30) | stop_after_attempt(3)), wait=wait_fixed(1))
async def call_model_gemini_with_tool(prompt, tools=None):
    try:
        gemini_client = GeminiAI(
            api_key=GeminiAiCFG.API_KEY,
            api_model=GeminiAiCFG.API_MODEL,
            tools=tools
        )
        generated_content = await gemini_client.generate_content(prompt)
        return generated_content
    except Exception as e:
        raise e


async def extract_function(fc_response):
    function_name = ""
    function_args = None
    if fc_response.candidates and fc_response.candidates[0].content:
        content = fc_response.candidates[0].content
        if content.parts and content.parts[0]:
            fc = content.parts[0]
            if fc.function_call:
                function_name = fc.function_call.name
                function_args = fc.function_call.args

    return {"function_name": function_name, "function_args": function_args}
