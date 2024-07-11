import traceback

from fastapi import APIRouter, File, UploadFile

from src.module.docs.docs_service import call_docs_handler
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/docs", tags=["docs"])


@router.post(path="/link", description="Upload html using link")
async def upload_docs_link_api(document_link: str):
    logger.info("------------------ API - Upload link")
    logger.info(f"MESSAGE: %s", document_link)
    try:
        response = await call_docs_handler(document_link=document_link)
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
async def upload_docs_file_api(document_file: UploadFile = File(..., description="File should be docx or pdf")):
    logger.info("------------------ API - Upload file")
    logger.info(f"MESSAGE: %s", document_file.filename)
    try:
        response = await call_docs_handler(document_file=document_file)
        return response
    except TimeoutError as err:
        # raise HTTPException(status_code=408, detail=err)
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
    except Exception as err:
        # raise HTTPException(status_code=500, detail=err)
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
