import json

from src.config.constant import ZillizCFG
from src.module.databases.zillizdb.zilliz_client import ZillizClient
from src.module.llm.embedding.gemini_embedding import GeminiEmbeddingModel
from src.utils.logger import logger


def insert_docs_to_zilliz(doc):
    try:
        document = document_builder(doc)
        zilliz = ZillizClient(ZillizCFG.ZILLIZDB_COLLECTION_NAME_DOCUMENTS)
        zilliz.insert_records([document])
        return {"status": True}
    except Exception as e:
        logger.error(e)
        return {"status": False}


def retrieve_docs_zilliz(event):
    doc_name = event.doc_name
    doc_tags = event.doc_tags
    doc_tags_str = ",".join(doc_tags)
    doc_query = f"{doc_name} {doc_tags_str}"
    doc_query = doc_query.lower().strip()
    logger.info("SEARCH QUERY: %s", doc_query)

    zilliz = ZillizClient()
    search_results = zilliz.vector_search(
        query=doc_query
    )
    search_results = search_results[0]
    logger.info(
        "SEARCH RESULT: %s",
        str(json.dumps(search_results, indent=4, ensure_ascii=False)),
    )

    docs = [item.get("entity").get("doc_id") for item in search_results]
    logger.info(
        "RETRIEVED DOCS: %s",
        str(json.dumps(docs, indent=4, ensure_ascii=False)),
    )

    response = {"docs": docs}
    return response


def document_builder(data):
    embedding = GeminiEmbeddingModel()

    doc_id = data.doc_id
    doc_name = data.doc_name.lower().strip()
    doc_content = data.doc_description

    doc_content_embedding = embedding.get_embedding(
        doc_content,
        task_type="retrieval_document",
        title="document"
    )

    document = {
        "id": doc_id,
        "source": doc_name,
        "title": doc_name,
        "content": doc_content,
        "language": "vi",
        "vector": doc_content_embedding.get("embedding"),
    }

    return document


def get_docs_qa_response(data, language):
    answer = "qa"
    question = data.sender_message
    return answer
