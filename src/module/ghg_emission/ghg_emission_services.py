import json
import time
from datetime import datetime

from src.config.constant import FirebaseCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_ghg_emission import PROMPT_GHG_EMISSION_PROCESS
from src.utils.logger import logger
from src.module.ghg_emission.ghg_emission_calculator import GHGEmissionCalculator


async def process_ghg_emission(data):
    formatted_prompt = PROMPT_GHG_EMISSION_PROCESS.format(
        facility_name=data.facility_name,
        plant=data.plant,
        period=f"{data.period_start} - {data.period_end}",
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


def calculate_ghg_emission(
        irrigation_data,
        organic_amendment_data,
        land_management_data,
        crop_protection_data,
        energy_data
):
    ghg_emission_calculator = GHGEmissionCalculator(
        irrigation_data=irrigation_data,
        organic_amendment_data=organic_amendment_data,
        land_management_data=land_management_data,
        crop_protection_data=crop_protection_data,
        energy_data=energy_data
    )
    (total_emission,
     irrigation_emission,
     land_management_emission,
     crop_protection_emission,
     energy_emission) = ghg_emission_calculator.calculate_emission()
    return {
        'total_emission': total_emission,
        'irrigation_emission': irrigation_emission,
        'land_management_emission': land_management_emission,
        'crop_protection_emission': crop_protection_emission,
        'energy_emission': energy_emission
    }


async def extract_emission_data(data):
    firestore = FirestoreWrapper()
    period_start = datetime.strptime(data.period_start, '%d/%m/%Y')
    period_end = datetime.strptime(data.period_end, '%d/%m/%Y')
    mrv_data = await firestore.retrieve_data(
        collection_name=FirebaseCFG.FS_COLLECTION_MRV,
        query_filters=[
            ("facility", "==", data.facility),
            ("date", "<=", period_end),
            ("date", ">=", period_start)
        ],
        order_by="date"
    )

    mrv_data = [{"date": datetime.strftime(item["date"], "%d/%m/%Y"), **item} for item in mrv_data]
    logger.info("mrv_data: %s", mrv_data)
    emission_data_response = {
        "length": len(mrv_data),
        "mrv_data": mrv_data
    }
    return emission_data_response
