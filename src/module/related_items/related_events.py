import json

from src.config.constant import ZillizCFG
from src.module.embedding.gemini_embedding import GeminiEmbeddingModel
from src.module.zillizdb.zilliz_client import ZillizClient
from src.utils.logger import logger


def insert_event_to_zilliz(event):
    try:
        document = document_builder(event)
        zilliz = ZillizClient(ZillizCFG.ZILLIZDB_COLLECTION_NAME_DOCUMENTS)
        zilliz.insert_records([document])
        return {"status": True}
    except Exception as e:
        logger.error(e)
        return {"status": False}


def retrieve_related_events_zilliz(event):
    event_name = event.event_name
    event_tags = event.event_tags
    event_tags_str = ",".join(event_tags)
    event_query = f"{event_name} {event_tags_str}"
    event_query = event_query.lower().strip()
    logger.info("SEARCH QUERY: %s", event_query)

    zilliz = ZillizClient()
    search_results = zilliz.vector_search(
        query=event_query
    )
    search_results = search_results[0]
    logger.info(
        "SEARCH RESULT: %s",
        str(json.dumps(search_results, indent=4, ensure_ascii=False)),
    )

    related_events = [item.get("entity").get("event_id") for item in search_results]
    logger.info(
        "RETRIEVED RELATED EVENTS: %s",
        str(json.dumps(related_events, indent=4, ensure_ascii=False)),
    )

    response = {"related_events": related_events}
    return response


def document_builder(data):
    embedding = GeminiEmbeddingModel()

    event_id = data.event_id
    event_name = data.event_name.lower().strip()
    event_tags = data.event_tags
    event_description = data.event_description

    event_info_embedding = embedding.get_embedding(
        event_description,
        task_type="retrieval_document",
        title="document"
    )

    document = {
        "id": event_id,
        "source": event_name,
        "title": event_tags,
        "content": event_description,
        "language": event_description,
        "embedding": event_info_embedding.get("embedding"),
    }

    return document
