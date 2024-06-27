from datetime import datetime

import mysql.connector
from mysql.connector import Error

from src.config.constant import MySQLCFG
from src.module.gemini.gemini_services import call_model_gemini
from src.module.gemini.prompts import PROMPT_REPORT
from src.utils.helpers import get_current_date
from src.utils.logger import logger


def connect_and_query(query):
    try:
        connection = mysql.connector.connect(
            host=MySQLCFG.MYSQL_HOST,
            database=MySQLCFG.MYSQL_DATABASE,
            user=MySQLCFG.MYSQL_USER,
            password=MySQLCFG.MYSQL_PASSWORD
        )

        if connection.is_connected():
            logger.info("Successfully connected to the database")
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            records = cursor.fetchall()
            logger.info("Total number of rows in result: %s", cursor.rowcount)
            cursor.close()
            connection.close()
            logger.info("MySQL connection is closed")
            return records
    except Error as e:
        print("Error while connecting to MySQL", e)


def query_report_data(inputs):
    current_date = str(get_current_date())
    # date = current_date
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

    metrics_str = ",".join(metrics)
    query = f'SELECT {metrics_str} FROM gathering WHERE datetime = "{date}";'
    logger.info("REPORT QUERY: %s", query)
    res = connect_and_query(query)
    return res


def gen_report_answer(report_data, language, report_info):
    formatted_prompt = PROMPT_REPORT.format(
        report_data=report_data,
        language=language,
        facility=report_info["facility"],
        plant=report_info["plant"],
        period=report_info["period"]
    )
    logger.info("PROMPT REPORT: %s", formatted_prompt)
    report_info_resp = call_model_gemini(formatted_prompt)
    logger.info("REPORT INFO: %s", report_info_resp)
    return report_info_resp
