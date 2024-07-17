import traceback
from typing import Any, Dict, Optional

from fastapi import APIRouter, File, Form, UploadFile

from src.models.scouting_model import ScoutingModel
from src.module.scouting.scouting_services import process_scouting_report
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/scouting", tags=["scouting"])


@router.post(path="/processReport")
async def process_scouting_report_api(
        facility: str = Form(""),
        plant: str = Form(""),
        date: str = Form(""),
        description: str = Form(""),
        file: Optional[UploadFile] = File(None)
) -> Dict[str, Any]:
    logger.info("------------------ API - Process scouting report")
    logger.info("MESSAGE: %s", description)
    logger.info("FILE: %s", file)
    try:
        data = ScoutingModel(facility=facility, plant=plant, date=date, description=description)
        response = await process_scouting_report(data, file)

        return response
    except Exception as err:
        logger.error("[X] Exception in process scouting report: %s, %s", err, traceback.format_exc())
        return {"response": "An error occurred while processing your request."}
