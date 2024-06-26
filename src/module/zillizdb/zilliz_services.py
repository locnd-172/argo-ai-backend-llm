import json

from src.config.constant import ZillizCFG
from src.module.zillizdb.zilliz_client import ZillizClient
from src.utils.logger import logger


def insert_documents_to_zilliz(documents):
    try:
        zilliz = ZillizClient(ZillizCFG.ZILLIZDB_COLLECTION_NAME_DOCUMENTS)
        zilliz.insert_records(documents)
        return True
    except Exception as e:
        logger.error(e)
        return False


def retrieve_documents_from_zilliz(query):
    logger.info("SEARCH QUERY: %s", query)

    zilliz = ZillizClient()
    search_results = zilliz.vector_search(query=query)
    search_results = search_results[0]
    logger.info(
        "SEARCH RESULT: %s",
        str(json.dumps(search_results, indent=4, ensure_ascii=False)),
    )

    return search_results
