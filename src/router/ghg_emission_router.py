import traceback
from typing import Any, Dict, List

from fastapi import APIRouter

from src.models.ghg_emission_model import GHGEmissionModel, Irrigation, Energy, CropProtection, LandManagament
from src.module.ghg_emission.ghg_emission_services import process_ghg_emission, calculate_ghg_emission
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

@router.post(path="/calculateEmission")
def calculate_emission_api(irrigation: Irrigation,
                          land_management: LandManagament,
                          crop_protection:  List[CropProtection],
                          energy: Energy):
    logger.info("------------------ API - Calculate GHG emission")
    # logger.info("EMISSION DATA: %s", data)
    try:
        response = calculate_ghg_emission(irrigation, land_management, crop_protection, energy)
        return None
    except Exception as err:
        logger.error("[X] Exception in calculate emission data: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}