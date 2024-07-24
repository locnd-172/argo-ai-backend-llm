import traceback

from fastapi import APIRouter, UploadFile, File

from src.models.docs_model import UploadLinkModel, UploadTextModel, DeleteDocumentModel, SearchDocumentModel
from src.module.docs.docs_service import call_docs_handler, get_all_docs, delete_docs_by_id, vector_search_docs
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
    logger.info(f"TITLE: %s", document.document_title)
    logger.info(f"TEXT: %s", document.document_text)
    try:
        response = await call_docs_handler(
            document_title=document.document_title,
            document_text=document.document_text,
        )
        return response
    except Exception as err:
        logger.error("[X] Exception in uploading docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}


@router.get(path="/getAllDocuments", description="Get all document from knowledgebase")
async def get_all_docs_api(collection: str):
    logger.info("------------------ API - Get all documents")
    try:
        response = await get_all_docs(collection)
        return response
    except Exception as err:
        logger.error("[X] Exception in get all docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}


@router.delete(path="/deleteDocumentById", description="delete document from knowledgebase")
async def delete_docs_by_id_api(data: DeleteDocumentModel):
    logger.info("------------------ API - Delete documents by Id")
    try:
        response = await delete_docs_by_id(data)
        return response
    except Exception as err:
        logger.error("[X] Exception in delete docs by id: %s, %s", err, traceback.format_exc())
        return {"result": False, "message": "Deleted Failed!"}


@router.post(path="/vectorSearch", description="Search relevant document")
async def vector_search_documents_api(inputs: SearchDocumentModel):
    logger.info("------------------ API - Search relevant documents")
    logger.info(f"SEARCH INPUT: %s", inputs)
    try:
        response = await vector_search_docs(inputs)
        return response
    except Exception as err:
        logger.error("[X] Exception in searching docs: %s, %s", err, traceback.format_exc())
        return {"response": "Unknown error"}
