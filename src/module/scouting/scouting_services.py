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
    return scouting_report_resp
