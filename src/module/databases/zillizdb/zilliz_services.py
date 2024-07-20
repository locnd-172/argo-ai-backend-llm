import json
import traceback

from src.config.constant import ZillizCFG
from src.module.databases.zillizdb.zilliz_client import ZillizClient
from src.utils.logger import logger


def insert_documents_to_zilliz(documents):
    filtered_item = [{key: value for key, value in item.items() if key != 'vector'} for item in documents]
    logger.info("filtered_item: %s", json.dumps(filtered_item, indent=4, ensure_ascii=False))
    try:
        zilliz = ZillizClient(ZillizCFG.ZILLIZDB_COLLECTION_NAME_DOCUMENTS)
        zilliz.insert_records(documents)
        return True
    except Exception as e:
        logger.error(e, traceback.format_exc())
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


def retrieve_all_documents_from_zilliz(index):
    zilliz = ZillizClient(collection_name=index)
    search_results = zilliz.get_all_documents()
    return search_results


def delete_documents_from_zilliz(ids=None, filters=""):
    zilliz = ZillizClient(collection_name=ZillizCFG.ZILLIZDB_COLLECTION_NAME_DOCUMENTS)
    delete_results = zilliz.delete_by_id(ids, filters)
    return delete_results
