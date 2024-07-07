import traceback
from typing import Any, Dict

from fastapi import APIRouter

from src.models.chat_model import ChatModel
from src.module.chat_response.generate_answer import generate_chat_response
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/docs", tags=["chat"])


@router.post(path="/insert")
def insert_docs_api(data: ChatModel) -> Dict[str, Any]:
    logger.info("------------------ API - Insert documents")
    logger.info(f"INPUT: %s", data)
    try:
        response = generate_chat_response(data)
        return response
    except TimeoutError as err:
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
    except Exception as err:
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
