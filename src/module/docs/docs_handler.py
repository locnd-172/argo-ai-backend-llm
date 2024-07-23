import time
import uuid

import pandas as pd

from src.config.constant import SourceType, DocumentStatus
from src.module.databases.zillizdb.zilliz_services import insert_documents_to_zilliz
from src.module.docs.docs_utils import split_documents, get_document_category
from src.module.llm.embedding.gemini_embedding import GeminiEmbeddingModel
from src.module.llm.text_splitters.html_splitter import split_html_from_url
from src.utils.helpers import get_text_size, extract_md_from_file
from src.utils.logger import logger


class DocsHandler:
    def __init__(
            self,
            document_file=None,
            document_link=None,
            document_text=None,
            document_title=None,
            document_id=None
    ):
        self.document_file = document_file
        self.document_link = document_link
        self.document_text = document_text
        self.document_title = document_title
        self.document_id = document_id
        self.embedding_model = GeminiEmbeddingModel()

    async def handle_document(self):
        document = None
        chunks = []
        title = ""
        source = ""
        language = "vietnamese"
        source_type = SourceType.TEXT
        if self.document_text is not None:
            document = self.document_text
            source = ""
            source_type = SourceType.TEXT
        elif self.document_file is not None:
            document = self.read_file()
            source = self.document_file.filename
            source_type = SourceType.FILE
        elif self.document_link is not None:
            document, chunks = self.read_url()
            source = self.document_link
            source_type = SourceType.URL
        else:
            logger.info('Invalid link or file')

        if document is None:
            return None

        try:
            title, language = await get_document_category(document)
        except Exception as e:
            logger.error("Error getting document title and language")

        title = self.document_title if self.document_title is not None else title

        logger.info("title: %s", title)
        logger.info("language: %s", language)

        if source_type != SourceType.URL:
            chunks = split_documents(content=document, document_type="md")

        logger.info("extracted chunks: %s", len(chunks))
        document_table = []
        for chunk in chunks:
            embedding = self.embedding_model.get_embedding(text=chunk, task_type="RETRIEVAL_DOCUMENT")
            chunk_content = f"{title}\n\n{chunk}"
            document_table.append({
                'id': str(uuid.uuid4()),
                'document_id': self.document_id,
                'vector': embedding['embedding'],
                'title': title,
                'content': chunk_content,
                'source': source,
                'language': language,
                'source_type': source_type,
                'source_size': get_text_size(document),
                'status': DocumentStatus.ACTIVE,
                'created_at': time.time(),
            })
        document_df = pd.DataFrame(document_table)
        insert_documents_to_zilliz(document_table)
        return document_df

    def read_file(self):
        content = extract_md_from_file(self.document_file.file)
        logger.info("File Content: %s", content)
        return content

    def read_url(self):
        chunks = split_html_from_url(self.document_link)
        content = "\n".join(chunks)
        return content, chunks
