import traceback
import uuid
from typing import Any, Dict, Optional

from fastapi import APIRouter, File, Form, UploadFile

from src.models.chat_model import ChatModel, HumanFeedbackModel
from src.module.chat_response.chat_statistic import get_chat_statistic
from src.module.chat_response.generate_answer import generate_chat_response
from src.module.chat_response.store_message import save_conversation
from src.module.chat_response.save_human_feedback import save_human_feedback
from src.utils import cache_history_service
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post(path="/generateAnswer")
async def generate_chat_response_api(
        message_id: str = Form(str(uuid.uuid4())),
        session_id: str = Form("1"),
        sender_id: str = Form("1"),
        sender_name: str = Form("anonymous"),
        sender_message: str = Form(""),
        file: Optional[UploadFile] = File(None)
) -> Dict[str, Any]:
    logger.info("------------------ API - Generate chat response")
    logger.info("MESSAGE: %s", sender_message)
    logger.info("FILE: %s", file)
    try:
        histories = cache_history_service.read_cache_by_session_id(session_id)

        data = ChatModel(
            message_id=message_id,
            session_id=session_id,
            sender_id=sender_id,
            sender_name=sender_name,
            sender_message=sender_message
        )
        response = await generate_chat_response(data, file, histories)

        await save_conversation(input_data=data, output_data=response)

        cache_history_service.write_cache(
            session_id=session_id,
            sender_data=sender_message,
            response=response.get("response")
        )
        return response
    except Exception as err:
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}


@router.post(path="/saveFeedbacks")
async def save_human_feedbacks_api(
        data: HumanFeedbackModel
) -> Dict[str, Any]:
    logger.info("------------------ API - Save human feedback")
    logger.info("FEEDBACK INPUT: %s", data)
    try:
        response = await save_human_feedback(data)
        return response
    except Exception as err:
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}


@router.get(path="/statistics")
async def get_chat_statistic_api() -> Dict[str, Any]:
    logger.info("------------------ API - Get conversation statistics")
    try:
        response = await get_chat_statistic()
        return response
    except Exception as err:
        logger.error("[X] Exception in generate answer: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}
