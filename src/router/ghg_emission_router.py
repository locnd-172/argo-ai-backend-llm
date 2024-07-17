import traceback
from typing import Any, Dict

from fastapi import APIRouter

from src.models.ghg_emission_model import GHGEmissionModel
from src.module.ghg_emission.ghg_emission_services import process_ghg_emission
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/emission", tags=["emission"])


@router.post(path="/processStatus")
async def process_emission_status_api(data: GHGEmissionModel) -> Dict[str, Any]:
    logger.info("------------------ API - Process GHG emission status")
    logger.info("EMISSION DATA: %s", data)
    try:
        response = await process_ghg_emission(data)
        return response
    except Exception as err:
        logger.error("[X] Exception in process emission data: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}
