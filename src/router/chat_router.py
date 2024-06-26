from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from src.models.chat_model import ChatModel
from src.module.chat_response.generate_answer import generate_chat_response
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post(path="/generateAnswer")
def generate_chat_response_api(data: ChatModel) -> Dict[str, Any]:
    logger.info("API - Generate chat response")
    try:
        response = generate_chat_response(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)

