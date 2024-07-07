import traceback

from fastapi import APIRouter, File, UploadFile
from typing import Annotated, Dict, Any, Optional, Union

from src.utils.logger import logger
from src.models.docs_model import DocsModel
from src.module.docs.docs_service import call_docs_handler

router = APIRouter(prefix="/api/v1/docs", tags=["docs"])


@router.post(path="/link", description="Upload html using link")
def upload_docs_link_api(document_link: str):
    logger.info("------------------ API - Upload link")
    logger.info(f"MESSAGE: %s", document_link)
    try:
        tmp = call_docs_handler(document_link=document_link)

        response = ""
        return response
    except TimeoutError as err:
        # raise HTTPException(status_code=408, detail=err)
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
    except Exception as err:
        # raise HTTPException(status_code=500, detail=err)
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}


@router.post(path="/file", description="Upload document using file")
def upload_docs_file_api(document_file: UploadFile = File(..., description="File should be docx or pdf")):
    logger.info("------------------ API - Upload file")
    logger.info(f"MESSAGE: %s", document_file.filename)
    try:
        tmp = call_docs_handler(document_file=document_file)

        response = ""
        return response
    except TimeoutError as err:
        # raise HTTPException(status_code=408, detail=err)
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
    except Exception as err:
        # raise HTTPException(status_code=500, detail=err)
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
