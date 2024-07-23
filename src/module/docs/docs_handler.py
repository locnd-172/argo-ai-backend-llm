import io
import time
import uuid

import pandas as pd
import requests
import asyncio
from bs4 import BeautifulSoup
from docx import Document
from pdfquery import PDFQuery

from src.config.constant import SourceType, DocumentStatus
from src.module.databases.zillizdb.zilliz_services import insert_documents_to_zilliz
from src.module.llm.embedding.gemini_embedding import GeminiEmbeddingModel
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_docs_process import PROMPT_CATEGORY_DOCUMENT
from src.utils.helpers import get_text_size
from src.utils.logger import logger
from src.utils.helpers import extract_md_from_file, remove_empty_lines


async def get_document_category(document):
    formatted_prompt = PROMPT_CATEGORY_DOCUMENT.format(document=document)
    response = await call_model_gemini(formatted_prompt)
    title = response['title']
    language = response['language']
    return title, language


class DocsHandler:
    def __init__(
            self,
            document_file=None,
            document_link=None,
            document_text=None,
            document_title=None,
            document_id=None
    ):
        self.chunk_step = 500
        self.document_file = document_file
        self.document_link = document_link
        self.document_text = document_text
        self.document_title = document_title
        self.source = ""
        self.source_type = SourceType.TEXT
        self.document_id = document_id
        self.embedding_model = GeminiEmbeddingModel()

    async def handle_document(self):
        document = None
        if self.document_text is not None:
            document = self.document_text
            self.source = ""
            self.source_type = SourceType.TEXT
        elif self.document_file is not None:
            if self.document_file.filename.endswith('.pdf') or self.document_file.filename.endswith('.docx'):
                document = await extract_md_from_file(self.document_file)
                self.source = self.document_file.filename
            self.source_type = SourceType.FILE
        elif self.document_link is not None:
            document = self.read_link()
            self.source = self.document_link
            self.source_type = SourceType.URL
        else:
            logger.info('Invalid link or file')

        if document is None:
            return None
        else:
            try:
                title, language = await get_document_category(document)
            except Exception as e:
                logger.error("Error getting document title and language")
                title, langauge = "", "vietnamese"

            document_size = get_text_size(document)
            if self.document_title is not None:
                title = self.document_title
            chunked_document = self.chunk_document(document)
            document_table = []
            for chunk in chunked_document:
                text = chunk
                id = str(uuid.uuid4())
                embedding = self.embedding_model.get_embedding(text=text, task_type="RETRIEVAL_DOCUMENT")
                document_table.append({
                    'id': id,
                    'document_id': self.document_id,
                    'vector': embedding['embedding'],
                    'title': title,
                    'content': text,
                    'source': self.source,
                    'language': language,
                    'source_type': self.source_type,
                    'source_size': document_size,
                    'status': DocumentStatus.ACTIVE,
                    'created_at': time.time(),
                })
            document_df = pd.DataFrame(document_table)
            insert_documents_to_zilliz(document_table)
            return document_df

    # def read_docx(self):
    #     file = io.BytesIO(self.document_file.file.read())
    #     doc = Document(file)
    #     full_text = []
    #     for para in doc.paragraphs:
    #         full_text.append(para.text)
    #     paragraph = ' '.join(full_text)
    #
    #     return paragraph

    # def read_pdf(self):
    #     file = io.BytesIO(self.document_file.file.read())
    #     pdf = PDFQuery(file)
    #     pdf.load()
    #
    #     text_elements = pdf.pq('LTTextLineHorizontal')
    #     text = [t.text for t in text_elements]
    #     paragraph = ' '.join(text)
    #
    #     return paragraph

    def pull_url(self):
        page = requests.get(self.document_link)
        soup = ""
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
        else:
            logger.info(f'The url {self.document_link} returned a status of {page.status_code}')
        return soup

    def read_link(self):
        soup = self.pull_url()
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        paragraph = '\n'.join(chunk for chunk in chunks if chunk)
        return paragraph

    def chunk_document(self, document):
        document = document.split(" ")
        N = len(document)
        step = self.chunk_step
        chunked_documents = []
        for i in range(0, N, step):
            chunked_document = ' '.join(' '.join(document[i:i + step]).splitlines())
            chunked_documents.append(chunked_document)

        return chunked_documents
