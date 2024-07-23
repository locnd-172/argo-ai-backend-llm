from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_docs_process import PROMPT_CATEGORY_DOCUMENT
from src.module.llm.text_splitters.html_splitter import split_html_from_url, split_markdown
from src.utils.logger import logger


async def get_document_category(document):
    formatted_prompt = PROMPT_CATEGORY_DOCUMENT.format(document=document)
    response = await call_model_gemini(formatted_prompt)
    title = response['title']
    language = response['language']
    return title, language


def split_documents(content, document_type):
    chunks = []
    if document_type == "md":
        logger.info("splitting markdown documents")
        chunks = split_markdown(content)
    elif document_type == "html":
        chunks = split_html_from_url(text=content)
    return chunks


def chunk_document(document):
    document = document.split(" ")
    N = len(document)
    step = 500
    chunked_documents = []
    for i in range(0, N, step):
        chunked_document = ' '.join(' '.join(document[i:i + step]).splitlines())
        chunked_documents.append(chunked_document)

    return chunked_documents
