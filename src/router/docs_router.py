import traceback

from fastapi import APIRouter, UploadFile, File

from src.models.docs_model import UploadLinkModel, UploadTextModel
from src.module.docs.docs_service import call_docs_handler
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/docs", tags=["docs"])


@router.post(path="/uploadLink", description="Upload html using link")
async def upload_docs_link_api(document: UploadLinkModel):
    logger.info("------------------ API - Upload link")
    logger.info(f"LINK: %s", document.document_link)
    try:
        response = await call_docs_handler(document_link=document.document_link)
        return response
    except Exception as err:
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}


@router.post(path="/uploadFile", description="Upload document using file")
async def upload_docs_file_api(document_file: UploadFile = File(..., description="File should be docx or pdf")):
    logger.info("------------------ API - Upload file")
    logger.info(f"FILE: %s", document_file)
    try:
        response = await call_docs_handler(document_file=document_file)
        return response
    except Exception as err:
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}


@router.post(path="/uploadText", description="Upload document using plain text")
async def upload_docs_text_api(document: UploadTextModel):
    logger.info("------------------ API - Upload text")
    logger.info(f"TEXT: %s", document.document_text)
    try:
        response = await call_docs_handler(document_text=document.document_text)
        return response
    except Exception as err:
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
