from datetime import datetime

from google.generativeai.types import Tool

from src.config.constant import FirebaseCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.module.llm.function_declaration.firestore_function import firestore_function_declaration
from src.module.llm.gemini.gemini_services import call_model_gemini, call_model_gemini_with_tool, extract_function
from src.module.llm.prompts.prompt_report import (
    PROMPT_EXTRACT_REPORT_INFO,
    PROMPT_REPORT, PROMPT_CALL_FUNCTION_GET_REPORT_INFO
)
from src.utils.helpers import get_current_date, get_current_year
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


async def gen_report_answer(report_data, language, metrics):
    formatted_prompt = PROMPT_REPORT.format(
        report_data=report_data,
        language=language,
        metrics=metrics
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


async def extract_report_info_by_function_calling(inputs):
    message = inputs.data.sender_message.lower()

    data_retrieval_tool = Tool(function_declarations=[firestore_function_declaration])
    tools = [data_retrieval_tool]

    formatted_prompt = PROMPT_CALL_FUNCTION_GET_REPORT_INFO.format(
        current_date=get_current_year(),
        user_message=message
    )
    report_info_resp = await call_model_gemini_with_tool(prompt=formatted_prompt, tools=tools)
    report_info_resp = await extract_function(report_info_resp)
    logger.info("function report info: %s", report_info_resp)

    function_name = report_info_resp["function_name"]
    function_args = report_info_resp["function_args"]
    function_args = dict(function_args)
    logger.info("function args: %s", function_args)

    query_filters = []
    facility = function_args.get("facility", "")
    date = function_args.get("date", "")
    metrics = function_args.get("metrics", "")

    logger.info(f"{facility} {date}")
    if facility not in "DEF_VALUE":
        query_filters.append(("facility", "==", facility))
    if date not in "DEF_VALUE":
        date_obj = datetime.strptime(date, '%d/%m/%Y')
        query_filters.append(("date", "==", date_obj))
    if metrics in "DEF_VALUE" or len(metrics) == 0:
        metrics = "irrigation, weather, soil, pest"

    logger.info("report query filters: %s", query_filters)
    if len(query_filters) == 0:
        return [], metrics

    mrv_data = []
    if function_name == "get_report_data":
        firestore = FirestoreWrapper()
        mrv_data = await firestore.retrieve_data(
            collection_name=FirebaseCFG.FS_COLLECTION_MRV,
            query_filters=query_filters,
            order_by="date" if date is None else None
        )

        logger.info("type mrv_data %s", type(mrv_data))
        if isinstance(mrv_data, list):
            mrv_data = mrv_data[:1] if len(mrv_data) > 1 else mrv_data
    logger.info("mrv_data: %s", mrv_data)
    return mrv_data, metrics


async def get_report_response(chat_request):
    logger.info("chat_request: %s", chat_request)
    report_data, metrics = await extract_report_info_by_function_calling(chat_request)
    report_resp = await gen_report_answer(
        report_data=report_data,
        language=chat_request.language,
        metrics=metrics
    )

    return report_resp
