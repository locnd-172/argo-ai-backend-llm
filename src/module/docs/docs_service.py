from src.module.docs.docs_handler import DocsHandler

def call_docs_handler(document_link = None, document_file = None):
    docs_handler = DocsHandler(document_link=document_link, document_file=document_file)
    # print(document_link)
    # print(document_file)
    document_table = docs_handler.handle_document()
    print(document_table)