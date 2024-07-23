import re
from typing import Any, List, Optional, Tuple

import pandas as pd
from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from constant import Chunking, Status
import uuid


class CustomizedMarkdownSplitter:
    def __init__(
            self,
            headers_to_split_on: List[Tuple[str, str]],
            return_each_line: bool = False,
            separators: Optional[List[str]] = None,
            keep_separator: bool = True,
            is_separator_regex: bool = False,
            **kwargs: Any,
    ):
        self.markdown_header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, return_each_line=return_each_line
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            keep_separator=keep_separator,
            is_separator_regex=is_separator_regex,
            chunk_size=1500,
        )

    def split_text(self, text: str, type: str):
        if type == "md":
            print("type md")
            splits = self.markdown_header_splitter.split_text(text)
            print("md splits")
            print(splits)
        else:
            splits = self.text_splitter.split_text(text)
        return splits


def merge_content(chunk, metadata):
    content = ""
    for i, key in enumerate(metadata):
        content += metadata[key] + "\n"
    content += chunk
    return content


def find_table(text: str):
    md_tables = list()
    html_tables = list()
    md_tables = re.findall(r"\n.*\|.*\|(\r?\n\|.*\|)+.*\r?\n", text, re.DOTALL)
    html_tables = re.findall(r"<table>.*?</table>", text, re.DOTALL)
    return md_tables, html_tables


def replace_for_list(content, value_replace, list):
    for item in list:
        content = content.replace(item, value_replace)
    return content


def break_html_table(table):
    thead_matches = re.findall(r"<thead>.*?</thead>", table, re.DOTALL)
    tbody_matches = re.findall(r"<tbody>.*?</tbody>", table, re.DOTALL)
    tr_value = tbody_matches[0].replace("<tbody>", "").replace("</tbody>", "")

    html_table_splitter = RecursiveCharacterTextSplitter(
        separators=["<tr>"],
        keep_separator=True,
        is_separator_regex=False,
        chunk_size=1400,
    )

    html_tables = []
    for item in html_table_splitter.split_text(tr_value):
        html_tables.append(
            "<table>\n"
            + thead_matches[0]
            + "\n<tbody>\n"
            + item
            + "\n</tbody>\n</table>"
        )
    return html_tables


def break_chunk(chunk, splitter):
    chunk_content = []
    for content in chunk:
        chunk_breaked = []
        lst_chunk = splitter.split_text(content, "text")
        if len(lst_chunk) > 1:
            md_tables, html_tables = find_table(content)
            content = replace_for_list(content, "", md_tables) if md_tables else content
            content = (
                replace_for_list(content, "", html_tables) if html_tables else content
            )

            chunk_breaked.extend(splitter.split_text(content, "text"))
            if md_tables:
                chunk_breaked.extend(md_tables)
            if html_tables:
                for table in html_tables:
                    chunk_breaked.extend(break_html_table(table))
        else:
            chunk_breaked.extend([content])
        chunk_content.append(chunk_breaked)
    return chunk_content


def create_id(row):
    return str(uuid.uuid4())


def process_chunk(documents, splitter):
    chunk = []
    metadata = []
    for document in documents:
        chunk.append(document.page_content)
        metadata.append((document.metadata))

    df = pd.DataFrame()
    df[Chunking.CHUNK] = break_chunk(chunk, splitter)
    df[Chunking.METADATA] = metadata
    df[Chunking.STATUS] = Status.DRAFT

    df = df.explode(Chunking.CHUNK, ignore_index=True)

    df[Chunking.CHUNK_ID] = df.apply(create_id, axis=1)
    df[Chunking.CHUNK_CONTENT] = df.apply(
        lambda x: merge_content(x.chunk, x.metadata), axis=1
    )
    df = df.drop(columns=[Chunking.CHUNK, Chunking.METADATA])
    print(f"Done processing chunk: {df.head(2)}")

    return df


def chunking_flow(md_content):
    splitter = CustomizedMarkdownSplitter(
        headers_to_split_on=Chunking.HEADERS_TO_SPLIT_ON,
        separators=Chunking.SEPARATORS,
        chunk_size=Chunking.CHUNK_SIZE,
        chunk_overlap=Chunking.CHUNK_OVERLAP,
    )
    splits = splitter.split_text(md_content, "md")
    df = process_chunk(splits, splitter)

    return df
