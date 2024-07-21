from src.module.databases.zillizdb.zilliz_services import (
    retrieve_all_documents_from_zilliz,
    delete_documents_from_zilliz
)
from src.module.docs.docs_handler import DocsHandler
from src.utils.logger import logger
import uuid


async def call_docs_handler(document_link=None, document_file=None, document_text=None, document_title=None):
    document_id = str(uuid.uuid4())
    docs_handler = DocsHandler(
        document_id=document_id,
        document_link=document_link,
        document_file=document_file,
        document_text=document_text,
        document_title=document_title,
    )
    document_df = await docs_handler.handle_document()
    logger.info("Length documents: %s", len(document_df))
    return {'STATUS': document_df is not None}


async def get_all_docs(collection_name):
    records = retrieve_all_documents_from_zilliz(collection_name)
    documents = []
    document_titles = []
    for record in records:
        title = record.get("title")
        if title not in document_titles:
            document_titles.append(title)
            document = {key: value for key, value in record.items() if key not in ["id"]}
            documents.append(document)

    logger.info("records length: %s", len(records))
    logger.info("documents length: %s", len(documents))
    return {"total": len(documents), "documents": documents}


async def delete_docs_by_id(data):
    document_ids = data.document_ids
    filter_str = f"document_id in {document_ids}"
    delete_result = delete_documents_from_zilliz(filters=filter_str)

    logger.info("delete result: %s", delete_result)
    if not delete_result:
        raise Exception("Fail to delete document by id %s" % document_ids)
    return {"result": delete_result, "message": "Deleted successfully"}
