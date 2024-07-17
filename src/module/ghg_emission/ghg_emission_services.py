from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_ghg_emission import PROMPT_GHG_EMISSION_PROCESS
from src.utils.logger import logger


async def process_ghg_emission(data):
    formatted_prompt = PROMPT_GHG_EMISSION_PROCESS.format(
        plant=data.plant,
        period=data.period,
        emission_data=data.emission_data
    )
    logger.info("PROMPT GHG EMISSION: {}".format(formatted_prompt))

    ghg_emission_resp = await call_model_gemini(formatted_prompt)
    logger.info("GHG EMISSION RESULT: %s", ghg_emission_resp)
    return ghg_emission_resp


async def process_emission_input(emission_data):
    emission_info = ""
    for key, value in emission_data.items():
        emission_info += f"{key}: {value}\n"
    return emission_info
