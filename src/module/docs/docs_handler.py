import io
import uuid

from src.utils.logger import logger

import json
from docx import Document
from pdfquery import PDFQuery

import requests
from bs4 import BeautifulSoup
import pandas as pd

from src.module.gemini.gemini_services import call_model_gemini
from src.module.gemini.prompts import PROMPT_PREPROCESS_HTML, PROMPT_CATEGORY_DOCUMENT
class DocsHandler:
    def __init__(self, document_file = None, document_link = None):
        self.chunk_step = 500
        self.document_file = document_file
        self.document_link = document_link
        self.source = ""
    def handle_document(self):
        document = None
        if self.document_file is not None:
            if self.document_file.filename.endswith('.pdf'):
                document = self.read_pdf()
                self.source = self.document_file.filename
                # print(document)
            elif self.document_file.filename.endswith('.docx'):
                document = self.read_docx()
                self.source = self.document_file.filename
                # print(document)
        elif self.document_link is not None:
            document = self.read_link()
            self.source = self.document_link
            # print(document)
        else:
            logger.info('Invalid link or file')
        if document is None:
            return None
        else:
            title, language = self.get_document_category(document)
            chunked_document = self.chunk_document(document)
            document_table = []
            for chunk in chunked_document:
                text = chunk
                id = str(uuid.uuid4())
                document_table.append({'id': id,
                                       'title': title,
                                       'language': language,
                                       'source': self.source,
                                       'text': text})
            document_df = pd.DataFrame(document_table)
            return document_df
            # print("CATEGORY: ", title, language)

    def read_docx(self):
        file = io.BytesIO(self.document_file.file.read())
        doc = Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        paragraph = ' '.join(full_text)

        return paragraph

    def read_pdf(self):
        file = io.BytesIO(self.document_file.file.read())
        pdf = PDFQuery(file)
        pdf.load()

        text_elements = pdf.pq('LTTextLineHorizontal')
        text = [t.text for t in text_elements]
        paragraph = ' '.join(text)

        return paragraph

    def pull_url(self):
        page = requests.get(self.document_link)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
        else:
            logger.info(f'The url {self.document_link} returned a status of {page.status_code}')
    def read_link(self):
        soup = self.pull_url()

        formatted_prompt = PROMPT_PREPROCESS_HTML.format(
            html_code=soup.prettify()
        )
        paragraph = call_model_gemini(formatted_prompt)['response']

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

    def get_document_category(self, document):
        formatted_prompt = PROMPT_CATEGORY_DOCUMENT.format(document=document)
        response = call_model_gemini(formatted_prompt)
        title = response['title']
        # category = response['category']
        language = response['language']

        return title, language