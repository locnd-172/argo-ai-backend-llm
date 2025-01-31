import traceback
from typing import Any, Dict

from fastapi import APIRouter

from src.models.emission_factors_model import EmissionFactorModel, UpdateEmissionFactorModel
from src.module.ghg_emission.emission_factors_services import get_all_emission_factors, insert_one_ef, update_one_ef, \
    delete_one_ef_by_id
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/emissionFactors", tags=["emission_factors"])


@router.get(path="/getAll")
async def get_all_api():
    logger.info("------------------ API - Get all EF")
    try:
        response = await get_all_emission_factors()
        return response
    except Exception as err:
        logger.error("[X] Exception in get all EF: %s, %s", err, traceback.format_exc())
        return []


@router.post(path="/addOne")
async def add_one_ef_api(data: EmissionFactorModel) -> Dict[str, Any]:
    logger.info("------------------ API - Add one EF")
    logger.info("ADD EF: %s", data)
    try:
        response = await insert_one_ef(data)
        return response
    except Exception as err:
        logger.error("[X] Exception in add one EF: %s, %s", err, traceback.format_exc())
        return {"result": False, "message": "An error occurred while inserting one emission factor."}


@router.post(path="/updateOne")
async def update_one_ef_api(data: UpdateEmissionFactorModel) -> Dict[str, Any]:
    logger.info("------------------ API - Update one EF")
    logger.info("UPDATE EF: %s", data)
    try:
        response = await update_one_ef(data=data)
        return response
    except Exception as err:
        logger.error("[X] Exception in update one EF: %s, %s", err, traceback.format_exc())
        return {"result": False, "message": "An error occurred while updating one emission factor."}


@router.delete(path="/deleteOneEFById")
async def delete_one_ef_by_id_api(document_id) -> Dict[str, Any]:
    logger.info("------------------ API - Delete one EF by ID")
    logger.info("DELETE EF ID: %s", document_id)
    try:
        response = await delete_one_ef_by_id(document_id=document_id)
        return response
    except Exception as err:
        logger.error("[X] Exception in delete one EF: %s, %s", err, traceback.format_exc())
        return {"result": False, "message": "An error occurred while deleting  one emission factor."}
