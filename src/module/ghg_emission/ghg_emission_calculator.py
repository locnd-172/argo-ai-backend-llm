import pandas as pd
import asyncio
from typing import Dict, Any, Tuple

from src.config.constant import EmissionCFG
from src.module.ghg_emission.emission_factors_services import get_all_emission_factors
from src.utils.logger import logger


async def get_ef_table() -> pd.DataFrame:
    ef_table = await get_all_emission_factors()
    return pd.DataFrame(ef_table)


class GHGEmissionCalculator:
    def __init__(
            self,
            irrigation_data: Any,
            organic_amendment_data: Any,
            land_management_data: Any,
            crop_protection_data: Any,
            energy_data: Any
    ) -> None:
        self.irrigation_data = irrigation_data
        self.organic_amendment_data = organic_amendment_data
        self.land_management_data = land_management_data
        self.crop_protection_data = crop_protection_data
        self.energy_data = energy_data
        self.ef_table = asyncio.run(get_ef_table())

    def calculate_emission(self) -> Tuple[float, float, float, float, float]:
        energy_emission = self.calculate_energy_emission()
        irrigation_emission = self.calculate_irrigation_emission()
        land_management_emission = self.calculate_land_management_emission()
        crop_protection_emission = self.calculate_crop_protection_emission()

        total_emission = (
                irrigation_emission +
                land_management_emission +
                crop_protection_emission +
                energy_emission
        )

        return total_emission, irrigation_emission, land_management_emission, crop_protection_emission, energy_emission

    def calculate_irrigation_emission(self) -> float:
        irrigation_ef = self.calculate_irrigation_factor()
        days_flooded = self.irrigation_data.days_flooded
        area = self.irrigation_data.area

        irrigation_emission_value = (
                area *
                irrigation_ef *
                days_flooded *
                EmissionCFG.CH4_CONVERSION_VALUE
        )
        return irrigation_emission_value

    def calculate_irrigation_factor(self) -> float:
        irrigation_ef = {"co2": 0, "ch4": 0, "n2o": 0}
        irrigation_mapping = {
            "is_continuous_flooding": "continuous_flooding",
            "is_single_aeration": "intermittent_flooding",
            "is_multiple_aeration": "intermittently_flooded_fields",
            "is_rainfed": "rainfed/deep_water",
            "is_upland": "upland"
        }

        for attr, ef_name in irrigation_mapping.items():
            if getattr(self.irrigation_data, attr, False):
                irrigation_ef = self.get_ef(ef_name)
                break

        logger.info("irrigation_ef: %s", irrigation_ef)
        irrigation_ef_ch4 = irrigation_ef.get("ch4", 0)

        scaling_factors = {
            "straw_incorporated_shortly": self.organic_amendment_data.straw_incorporated_short_value,
            "straw_incorporated_long": self.organic_amendment_data.straw_incorporated_long_value,
            "compost": self.organic_amendment_data.compost_value,
            "farm_yard_manure": self.organic_amendment_data.farm_yard_manure_value,
            "green_manure": self.organic_amendment_data.green_manure_value
        }

        scaling_factor = sum(
            value * self.get_ef(ef_name)['ch4']
            for ef_name, value in scaling_factors.items()
        ) + 1

        adjusted_irrigation_ef = irrigation_ef_ch4 * scaling_factor ** EmissionCFG.SCALING_FACTOR_VALUE
        return adjusted_irrigation_ef

    def calculate_land_management_emission(self) -> float:
        return self.calculate_emission_for_activities([
            ("synthetic_fertilizer", self.land_management_data.fertilizer_value),
            ("animal_manure", self.land_management_data.animal_manure_value),
            ("landfilling", self.land_management_data.landfill_value),
            ("incineration", self.land_management_data.incineration_value),
            ("burning_crop", self.land_management_data.crop_burning_value),
            ("composting", self.land_management_data.composting_value)
        ])

    def calculate_crop_protection_emission(self) -> float:
        return self.calculate_emission_for_activities([
            ("pesticide", self.crop_protection_data.pesticide_value),
            ("herbicide", self.crop_protection_data.herbicide_value),
            ("fungicide", self.crop_protection_data.fungicide_value),
            ("insecticide", self.crop_protection_data.insecticide_value)
        ])

    def calculate_energy_emission(self) -> float:
        return self.calculate_emission_for_activities([
            ("diesel", self.energy_data.diesel_value),
            ("gasoline", self.energy_data.gasoline_value),
            ("electricity", self.energy_data.electricity_value)
        ])

    def calculate_emission_for_activities(self, activities: list[Tuple[str, float]]) -> float:
        total_emission = 0
        for name, value in activities:
            ef = self.get_ef(name)
            total_emission += (
                    value * ef['co2'] +
                    value * ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE +
                    value * ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE
            )
        return total_emission

    def get_ef(self, name: str) -> Dict[str, float]:
        ef_values = self.ef_table.loc[
            self.ef_table['identity_title'].str.lower() == name.lower(),
            ['co2', 'ch4', 'n2o']
        ].squeeze()

        emission_value = ef_values.fillna(0).to_dict()
        logger.info("%s: %s", name, emission_value)
        return emission_value
