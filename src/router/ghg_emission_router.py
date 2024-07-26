import asyncio
import traceback
from typing import Any, Dict

from fastapi import APIRouter

from src.models.ghg_emission_model import (
    GHGEmissionModel,
    Irrigation,
    Energy,
    CropProtection,
    LandManagement,
    OrganicAmendment,
    EmissionFacility
)
from src.module.ghg_emission.ghg_emission_services import (
    process_ghg_emission,
    calculate_ghg_emission,
    extract_emission_data
)
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
def calculate_emission_api(
        facility: EmissionFacility,
        irrigation: Irrigation,
        organic_amendment: OrganicAmendment,
        land_management: LandManagement,
        crop_protection: CropProtection,
        energy: Energy
) -> Dict[str, Any]:
    logger.info("------------------ API - Calculate GHG emission")
    try:
        emission_data = calculate_ghg_emission(irrigation, organic_amendment, land_management, crop_protection, energy)

        emission_result = GHGEmissionModel(
            facility=facility.facility_name,
            plant=facility.plant,
            period_start=facility.period_start,
            period_end=facility.period_end,
            emission_data=emission_data
        )
        emission_evaluation = asyncio.run(process_ghg_emission(emission_result))
        return {"emission_evaluation": emission_evaluation, "emission_result": emission_result}
    except Exception as err:
        logger.error("[X] Exception in calculate emission data: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}


@router.post(path="/extractEmissionData")
async def extract_emission_data_api(data: GHGEmissionModel) -> Dict[str, Any]:
    logger.info("------------------ API - Extract emission data")
    logger.info("EMISSION FACILITY: %s", data)
    try:
        response = await extract_emission_data(data)
        return response
    except Exception as err:
        logger.error("[X] Exception in extract emission data: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}
