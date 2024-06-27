import traceback
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from src.models.chat_model import ChatModel
from src.module.cache import cache_history_service
from src.module.chat_response.generate_answer import generate_chat_response
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post(path="/generateAnswer")
def generate_chat_response_api(data: ChatModel) -> Dict[str, Any]:
    logger.info("------------------ API - Generate chat response")
    logger.info(f"MESSAGE: %s", data)
    try:
        session = data.session_id or "1"
        message = data.sender_message or ""
        histories = cache_history_service.read_cache_by_session_id(session)
        response = generate_chat_response(data, histories)
        cache_history_service.write_cache(
            session_id=session,
            sender_data=message,
            response=response.get("response")
        )
        return response
    except TimeoutError as err:
        # raise HTTPException(status_code=408, detail=err)
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
    except Exception as err:
        # raise HTTPException(status_code=500, detail=err)
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
