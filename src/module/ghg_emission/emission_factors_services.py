import json
import time
from datetime import datetime

from src.config.constant import FirebaseCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.utils.logger import logger


async def get_all_emission_factors():
    firestore = FirestoreWrapper()
    emission_factors = await firestore.retrieve_data(FirebaseCFG.FS_COLLECTION_EMISSION_FACTORS)

    # handle missing field
    for item in emission_factors:
        if "created_time" not in item or not isinstance(item["created_time"], (int, float)):
            item["created_time"] = str(time.time())

    sorted_emission_factors = sorted(
        emission_factors,
        key=lambda ef_item: datetime.fromtimestamp(ef_item["created_time"]),
        reverse=True
    )
    # logger.info(f"SORTED EF LIST: %s", json.dumps(sorted_emission_factors, indent=2))
    logger.info(f"SORTED EF LENGTH: %s", len(sorted_emission_factors))
    return sorted_emission_factors


async def insert_one_ef(data):
    insert_data = dict(data)
    insert_data["created_time"] = time.time()
    logger.info("INSERT DATA: %s", insert_data)

    firestore = FirestoreWrapper()
    insert_result = await firestore.insert_data(
        collection_name=FirebaseCFG.FS_COLLECTION_EMISSION_FACTORS,
        data=insert_data,
    )
    logger.info("INSERT RESULT: %s", insert_result)

    insert_response = {
        "result": True,
        "message": "Insert EF data successfully",
        "document_id": insert_result
    }
    return insert_response


async def update_one_ef(data):
    document_id = data.document_id
    update_data = dict(data)
    update_data["created_time"] = time.time()
    logger.info("UPDATE DATA: %s", update_data)
    del update_data["document_id"]

    firestore = FirestoreWrapper()
    update_result = await firestore.update_document(
        collection_name=FirebaseCFG.FS_COLLECTION_EMISSION_FACTORS,
        document_id=document_id,
        updated_data=update_data,
    )
    logger.info("UPDATE RESULT: %s", update_result)

    update_response = {
        "result": True,
        "message": "Update EF data successfully",
        "document_id": update_result
    }
    return update_response


async def delete_one_ef_by_id(document_id):
    firestore = FirestoreWrapper()
    delete_result = await firestore.delete_document(
        collection_name=FirebaseCFG.FS_COLLECTION_EMISSION_FACTORS,
        document_id=document_id,
    )
    logger.info("DELETE RESULT: %s", delete_result)

    delete_response = {
        "result": delete_result,
        "message": "Delete EF data successfully",
        "document_id": document_id
    }
    return delete_response
