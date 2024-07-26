from datetime import datetime

import pandas as pd

from src.config.constant import FirebaseCFG
from src.module.databases.firebase.firestore import FirestoreWrapper
from src.module.ghg_emission.ghg_emission_calculator import GHGEmissionCalculator
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_ghg_emission import PROMPT_GHG_EMISSION_PROCESS
from src.utils.logger import logger


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


async def fetch_mrv_data(data):
    period_start = datetime.strptime(data.period_start, '%d/%m/%Y')
    period_end = datetime.strptime(data.period_end, '%d/%m/%Y')
    firestore = FirestoreWrapper()
    return await firestore.retrieve_data(
        collection_name=FirebaseCFG.FS_COLLECTION_MRV,
        query_filters=[
            ("facility", "==", data.facility),
            ("date", "<=", period_end),
            ("date", ">=", period_start)
        ],
        order_by="date"
    )


def aggregate_emission_data(mrv_data):
    energy_totals = {"gasoline": 0, "diesel": 0, "electricity": 0}
    water_totals = {"days_flooded": 0, "water_consumed": 0, "water_recycled": 0}
    irrigation_types = set()

    for item in mrv_data:
        irrigation_data = item["data"]["irrigation"]
        energy_data = item["data"]["energy"]

        water_totals["days_flooded"] += irrigation_data["days_flooded"]
        water_totals["water_consumed"] += irrigation_data["water_consumed"]
        water_totals["water_recycled"] += irrigation_data["water_recycled"]
        energy_totals["gasoline"] += energy_data["gasoline"]
        energy_totals["diesel"] += energy_data["diesel"]
        energy_totals["electricity"] += energy_data["electricity"]

        irrigation_types.add(irrigation_data["irrigation_type"])

    irrigation_types = list(irrigation_types)
    irrigation_type = irrigation_types[0] if len(irrigation_types) > 0 else "continuous_flooding"

    return {
        "energy": energy_totals,
        "water": water_totals,
        "irrigation_type": irrigation_type
    }


async def extract_emission_data(data):
    mrv_data = await fetch_mrv_data(data)
    logger.info("mrv_data: %s", mrv_data)

    emission_data = aggregate_emission_data(mrv_data)
    logger.info("emission_data: %s", emission_data)

    return emission_data
