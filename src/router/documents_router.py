from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from src.models.documents_model import DocumentsModel, QueryDocumentsModel
from src.module.related_items.related_events import (
    insert_event_to_zilliz,
    retrieve_related_events_zilliz
)
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/documents", tags=["zilliz_documents"])


@router.post(path="/insert")
def insert_documents_api(data: DocumentsModel) -> Dict[str, Any]:
    logger.info("API - Insert documents to Zilliz")
    try:
        response = insert_event_to_zilliz(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.post(path="/retrieve")
def get_documents_api(data: QueryDocumentsModel) -> Dict[str, Any]:
    logger.info("API - Retrieve documents")
    try:
        response = retrieve_related_events_zilliz(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)
