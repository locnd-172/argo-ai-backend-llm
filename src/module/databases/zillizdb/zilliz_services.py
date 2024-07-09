import json

from src.config.constant import ZillizCFG
from src.module.databases.zillizdb.zilliz_client import ZillizClient
from src.utils.logger import logger


def insert_documents_to_zilliz(documents):
    try:
        zilliz = ZillizClient(ZillizCFG.ZILLIZDB_COLLECTION_NAME_DOCUMENTS)
        zilliz.insert_records(documents)
        return True
    except Exception as e:
        logger.error(e)
        return False


def retrieve_documents_from_zilliz(index, query, top_k):
    logger.info("SEARCH QUERY: %s", query)

    zilliz = ZillizClient(collection_name=index)
    search_results = zilliz.vector_search(query=query, limit_num=top_k)
    search_results = search_results[0]
    extracted_search_results = [item["entity"] for item in search_results]
    logger.info(
        "SEARCH RESULT: %s",
        str(json.dumps(extracted_search_results, indent=4, ensure_ascii=False)),
    )

    return extracted_search_results
