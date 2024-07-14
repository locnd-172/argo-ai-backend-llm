import traceback
from typing import Any, Dict, Optional

from fastapi import APIRouter, File, Form, UploadFile

from src.models.chat_model import ChatModel
from src.module.chat_response.generate_answer import generate_chat_response
from src.utils import cache_history_service
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post(path="/generateAnswer")
async def generate_chat_response_api(
        session_id: str = Form("1"),
        sender_message: str = Form(""),
        file: Optional[UploadFile] = File(None)
) -> Dict[str, Any]:
    logger.info("------------------ API - Generate chat response")
    logger.info("MESSAGE: %s", sender_message)
    logger.info("FILE: %s", file)
    try:
        histories = cache_history_service.read_cache_by_session_id(session_id)

        data = ChatModel(session_id=session_id, sender_message=sender_message)
        response = await generate_chat_response(data, file, histories)

        cache_history_service.write_cache(
            session_id=session_id,
            sender_data=sender_message,
            response=response.get("response")
        )
        return response
    except Exception as err:
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}
