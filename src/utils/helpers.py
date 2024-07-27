import asyncio
import re
from datetime import datetime

import fitz
import pymupdf4llm
import requests
from bs4 import BeautifulSoup

from src.utils.logger import logger


def pull_url(document_link):
    page = requests.get(document_link)
    soup = ""
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        logger.info(f'The url {document_link} returned a status of {page.status_code}')
    return soup


def extract_md_from_file(document_file):
    file_content = document_file.read()
    pdf_document = fitz.open(stream=file_content, filetype="pdf")
    md_text = pymupdf4llm.to_markdown(pdf_document)
    md_text = remove_empty_lines(md_text)
    return md_text


def remove_empty_lines(paragraph):
    cleaned_paragraph = re.sub(r"\n\s*\n", "\n", paragraph)
    return cleaned_paragraph.strip()


def get_text_size(text, encoding='utf-8'):
    encoded_text = text.encode(encoding)
    size_in_bytes = len(encoded_text)
    size_in_megabytes = round(size_in_bytes / (1024 * 1024), 4)
    return size_in_megabytes


def get_current_year():
    now = datetime.now()
    formatted_time = now.strftime("%Y")
    return formatted_time


def get_current_date():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y")
    return formatted_time


def get_current_datetime():
    now = datetime.now()
    formatted_time = now.strftime("%A, %d/%m/%Y %H:%M:%S")
    return formatted_time
