import json

from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_scouting import PROMPT_PROCESS_SCOUTING_REPORT
from src.utils.logger import logger


async def process_scouting_report(data, file):
    formatted_prompt = PROMPT_PROCESS_SCOUTING_REPORT.format(
        facility=data.facility,
        plant=data.plant,
        datetime=data.date,
        description=data.description
    )
    logger.info("PROMPT PROCESS SCOUTING REPORT: {}".format(formatted_prompt))

    scouting_report_resp = await call_model_gemini(formatted_prompt)
    logger.info("SCOUTING REPORT: %s", scouting_report_resp)

    scouting_report = {
        "facility": data.facility,
        "plant": data.plant,
        "datetime": data.date,
        "description": data.description,
        "health": scouting_report_resp.get("health_evaluation", "neutral"),
        "assessment": scouting_report_resp.get("assessment", ""),
        "suggestion": scouting_report_resp.get("suggestion", ""),
        "growth": {
            "report": scouting_report_resp.get("growth_report", ""),
            "status": scouting_report_resp.get("growth_status", "neutral")
        },
        "soil": {
            "report": scouting_report_resp.get("soil_report", ""),
            "status": scouting_report_resp.get("soil_status", "neutral")
        },
        "water": {
            "report": scouting_report_resp.get("water_report", ""),
            "status": scouting_report_resp.get("water_status", "neutral")
        },
        "pest": {
            "report": scouting_report_resp.get("pest_report", ""),
            "status": scouting_report_resp.get("pest_status", "neutral")
        },
        "disease": {
            "report": scouting_report_resp.get("disease_report", ""),
            "status": scouting_report_resp.get("disease_status", "neutral")
        },
        "other_report": scouting_report_resp.get("other_report", ""),
    }
    logger.info("SCOUTING REPORT: %s", json.dumps(scouting_report, indent=4, ensure_ascii=False))

    return scouting_report_resp
