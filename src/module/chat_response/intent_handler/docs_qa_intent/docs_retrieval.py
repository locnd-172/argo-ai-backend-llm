from src.module.databases.zillizdb.zilliz_services import \
    retrieve_documents_from_zilliz
from src.utils.logger import logger


def call_search_vector_hybrid(inputs):
    search_result = []
    try:
        search_result = retrieve_documents_from_zilliz(
            index=inputs.index,
            query=inputs.search,
            top_k=inputs.top
        )
    except Exception as e:
        logger.error(f"ERROR HYBRID SEARCH: {e}")

    return search_result
