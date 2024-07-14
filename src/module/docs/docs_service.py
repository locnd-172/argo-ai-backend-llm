import json

from src.module.databases.zillizdb.zilliz_services import retrieve_all_documents_from_zilliz
from src.module.docs.docs_handler import DocsHandler
from src.utils.logger import logger


async def call_docs_handler(document_link=None, document_file=None, document_text=None):
    docs_handler = DocsHandler(
        document_link=document_link,
        document_file=document_file,
        document_text=document_text,
    )
    document_df = await docs_handler.handle_document()
    logger.info("Length documents: %s", len(document_df))
    return {'STATUS': document_df is not None}


async def call_get_docs(collection_name):
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
