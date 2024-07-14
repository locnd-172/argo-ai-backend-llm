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
