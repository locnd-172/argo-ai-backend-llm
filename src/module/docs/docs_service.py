from src.module.docs.docs_handler import DocsHandler


async def call_docs_handler(document_link=None, document_file=None):
    docs_handler = DocsHandler(document_link=document_link, document_file=document_file)
    document_df = await docs_handler.handle_document()

    return {'STATUS': 'SUCCESS',
            'CONTENT': None}
    # document_table = await docs_handler.handle_document()
    # print(document_table)
