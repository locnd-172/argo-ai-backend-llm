from datetime import datetime

from src.config.constant import FirebaseCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_report import (
    PROMPT_EXTRACT_REPORT_INFO,
    PROMPT_REPORT
)
from src.utils.helpers import get_current_date
from src.utils.logger import logger


async def query_report_data(inputs):
    current_date = str(get_current_date())
    logger.info("CURRENT DATE: %s", current_date)
    date_str = inputs.get("period", current_date)
    date_object = datetime.strptime(date_str, "%d/%m/%Y")
    date = date_object.strftime("%d/%m/%Y")
    logger.info("REPORT DATE: %s", date)

    input_metrics = inputs.get('metrics', "soil, water, weather")
    metrics = []
    if "soil" in input_metrics.lower():
        metrics.extend(["soil_moisture", "soil_temperature", "soil_pH", "soil_conductivity"])
    if "water" in input_metrics.lower():
        metrics.extend(["water_consumed", "water_recycled", "water_quality"])
    if "weather" in input_metrics.lower():
        metrics.extend(["max_temperature", "min_temperature", "wind", "wind_direction", "humidity", "cloud",
                        "atmospheric_pressure"])

    firestore = FirestoreWrapper()
    mrv_data = await firestore.retrieve_data(
        collection_name=FirebaseCFG.FS_COLLECTION_MRV,
        query_filters=[("date", "=", date)]
    )

    logger.info("REPORT DATA: %s", mrv_data)
    return mrv_data


async def gen_report_answer(report_data, language, report_info):
    formatted_prompt = PROMPT_REPORT.format(
        report_data=report_data,
        language=language,
        facility=report_info["facility"],
        plant=report_info["plant"],
        period=report_info["period"]
    )
    logger.info("PROMPT REPORT: %s", formatted_prompt)
    report_info_resp = await call_model_gemini(formatted_prompt)
    logger.info("REPORT INFO: %s", report_info_resp)
    return report_info_resp


async def extract_report_info(data):
    formatted_prompt = PROMPT_EXTRACT_REPORT_INFO.format(message=data.sender_message)
    report_info_resp = await call_model_gemini(formatted_prompt)
    logger.info("REPORT INFO: %s", report_info_resp)
    return report_info_resp


async def get_report_response(chat_request):
    report_info = await extract_report_info(data=chat_request.data)
    report_data = await query_report_data(report_info)
    report_resp = await gen_report_answer(
        report_data=report_data,
        language=chat_request.language,
        report_info=report_info
    )

    return report_resp
