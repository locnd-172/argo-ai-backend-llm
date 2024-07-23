from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import HTMLHeaderTextSplitter, MarkdownHeaderTextSplitter

from src.config.constant import TextSplitterCFG
from src.utils.logger import logger


def split_markdown(markdown_text):
    markdown_header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=TextSplitterCFG.MD_HEADERS_TO_SPLIT_ON,
        return_each_line=False
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TextSplitterCFG.WORD_CHUNK_SIZE,
        separators=TextSplitterCFG.SEPARATORS,
        keep_separator=True,
        is_separator_regex=False,
    )
    splits = markdown_header_splitter.split_text(markdown_text)
    splits = text_splitter.split_documents(splits)

    logger.info("splits len: %s", len(splits))
    chunks = process_chunks(chunks=splits, doc_type="md")
    return chunks


def split_html_from_url(url=None, text=None):
    html_splitter = HTMLHeaderTextSplitter(
        headers_to_split_on=TextSplitterCFG.HTML_HEADERS_TO_SPLIT_ON
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TextSplitterCFG.WORD_CHUNK_SIZE,
        chunk_overlap=TextSplitterCFG.CHUNK_OVERLAP
    )

    html_header_splits = []
    if url is not None:
        html_header_splits = html_splitter.split_text_from_url(url)
    elif text is not None:
        html_header_splits = html_splitter.split_text(text)

    splits = text_splitter.split_documents(html_header_splits)

    chunks = process_chunks(chunks=splits, doc_type="html")
    return chunks


def process_chunks(chunks, doc_type):
    processed_chunks = []
    for chunk in chunks:
        metadata = chunk.metadata
        chunk_content = chunk.page_content

        header1 = metadata.get("h1", "")
        header2 = metadata.get("h2", "")
        header3 = metadata.get("h3", "")
        header4 = metadata.get("h4", "")

        if header4:
            chunk_content = f"#### {header4}\n{chunk_content}"
        if header3:
            chunk_content = f"### {header3}\n{chunk_content}"
        if header2:
            chunk_content = f"## {header2}\n{chunk_content}"
        if header1:
            chunk_content = f"# {header1}\n{chunk_content}"

        if doc_type == "html" and len(metadata) == 0:
            continue

        processed_chunks.append(chunk_content)
    return processed_chunks
