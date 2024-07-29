import pandas as pd
import asyncio

from src.config.constant import EmissionCFG
from src.module.ghg_emission.emission_factors_services import get_all_emission_factors
from src.utils.logger import logger


def get_ef_table():
    ef_table = asyncio.run(get_all_emission_factors())
    ef_table = pd.DataFrame(ef_table)
    return ef_table


class GHGEmissionCalculator:
    def __init__(
            self,
            irrigation_data,
            organic_amendment_data,
            land_management_data,
            crop_protection_data,
            energy_data
    ):
        self.irrigation_data = irrigation_data
        self.organic_amendment_data = organic_amendment_data
        self.land_management_data = land_management_data
        self.crop_protection_data = crop_protection_data
        self.energy_data = energy_data
        self.ef_table = get_ef_table()

    def calculate_emission(self):
        irrigation_emission = self.calculate_irrigation_emission()
        land_management_emission = self.calculate_land_management_emission()
        crop_protection_emission = self.calculate_crop_protection_emission()
        energy_emission = self.calculate_energy_emission()

        total_emission = irrigation_emission + land_management_emission + crop_protection_emission + energy_emission

        irrigation_emission = round(irrigation_emission, 2)
        land_management_emission = round(land_management_emission, 2)
        crop_protection_emission = round(crop_protection_emission, 2)
        energy_emission = round(energy_emission, 2)
        total_emission = round(total_emission, 2)

        return total_emission, irrigation_emission, land_management_emission, crop_protection_emission, energy_emission

    def calculate_irrigation_emission(self):
        irrigation_ef = self.calculate_irrigation_factor()
        days_flooded = self.irrigation_data.days_flooded
        area = self.irrigation_data.area

        irrigation_emission_value = area * irrigation_ef * days_flooded * EmissionCFG.CH4_CONVERSION_VALUE
        return irrigation_emission_value

    def calculate_irrigation_factor(self):
        irrigation_ef = {"co2": 0, "ch4": 0, "n2o": 0}
        if self.irrigation_data.is_continuous_flooding:
            irrigation_ef = self.get_ef("continuous_flooding")
        elif self.irrigation_data.is_single_aeration:
            irrigation_ef = self.get_ef("intermittent_flooding")
        elif self.irrigation_data.is_multiple_aeration:
            irrigation_ef = self.get_ef("intermittently_flooded_fields")
        elif self.irrigation_data.is_rainfed:
            irrigation_ef = self.get_ef("rainfed/deep_water")
        elif self.irrigation_data.is_upland:
            irrigation_ef = self.get_ef("upland")

        logger.info("irrigation_ef: %s", irrigation_ef)
        irrigation_ef = irrigation_ef.get("ch4", 0)

        scaling_factor = 1
        straw_incorporated_short_ef = self.get_ef("straw_incorporated_shortly")['ch4']
        straw_incorporated_short_value = self.organic_amendment_data.straw_incorporated_short_value
        scaling_factor += straw_incorporated_short_value * straw_incorporated_short_ef

        straw_incorporated_long_ef = self.get_ef("straw_incorporated_long")['ch4']
        straw_incorporated_long_value = self.organic_amendment_data.straw_incorporated_long_value
        scaling_factor += straw_incorporated_long_value * straw_incorporated_long_ef

        compost_ef = self.get_ef("compost")['ch4']
        compost_value = self.organic_amendment_data.compost_value
        scaling_factor += compost_value * compost_ef

        farm_yard_manure_ef = self.get_ef("farm_yard_manure")['ch4']
        farm_yard_manure_value = self.organic_amendment_data.farm_yard_manure_value
        scaling_factor += farm_yard_manure_value * farm_yard_manure_ef

        green_manure_ef = self.get_ef("green_manure")['ch4']
        green_manure_value = self.organic_amendment_data.green_manure_value
        scaling_factor += green_manure_value * green_manure_ef

        adjusted_irrigation_ef = irrigation_ef * pow(scaling_factor, EmissionCFG.SCALING_FACTOR_VALUE)

        return adjusted_irrigation_ef

    def calculate_land_management_emission(self):
        land_management_emission = 0

        fertilizer_ef = self.get_ef("synthetic_fertilizer")
        fertilizer_value = self.land_management_data.fertilizer_value
        land_management_emission += (fertilizer_value * fertilizer_ef['co2']
                                     + fertilizer_value * fertilizer_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + fertilizer_value * fertilizer_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        animal_manure_ef = self.get_ef("animal_manure")
        animal_manure_value = self.land_management_data.animal_manure_value
        land_management_emission += (animal_manure_value * animal_manure_ef['co2']
                                     + animal_manure_value * animal_manure_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + animal_manure_value * animal_manure_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        landfill_ef = self.get_ef("landfilling")
        landfill_value = self.land_management_data.landfill_value
        land_management_emission += (landfill_value * landfill_ef['co2']
                                     + landfill_value * landfill_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + landfill_value * landfill_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        incineration_ef = self.get_ef("incineration")
        incineration_value = self.land_management_data.incineration_value
        land_management_emission += (incineration_value * incineration_ef['co2']
                                     + incineration_value * incineration_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + incineration_value * incineration_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        crop_burning_ef = self.get_ef("burning_crop")
        crop_burning_value = self.land_management_data.crop_burning_value
        land_management_emission += (crop_burning_value * crop_burning_ef['co2']
                                     + crop_burning_value * crop_burning_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + crop_burning_value * crop_burning_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        composting_ef = self.get_ef("composting")
        composting_value = self.land_management_data.composting_value
        land_management_emission += (composting_value * composting_ef['co2']
                                     + composting_value * composting_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + composting_value * composting_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        return land_management_emission

    def calculate_crop_protection_emission(self):
        crop_protection_emission = 0

        pesticide_ef = self.get_ef("pesticide")
        pesticide_value = self.crop_protection_data.pesticide_value
        crop_protection_emission += (pesticide_value * pesticide_ef['co2']
                                     + pesticide_value * pesticide_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + pesticide_value * pesticide_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        herbicide_ef = self.get_ef("herbicide")
        herbicide_value = self.crop_protection_data.herbicide_value
        crop_protection_emission += (herbicide_value * herbicide_ef['co2']
                                     + herbicide_value * herbicide_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + herbicide_value * herbicide_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        fungicide_ef = self.get_ef("fungicide")
        fungicide_value = self.crop_protection_data.fungicide_value
        crop_protection_emission += (fungicide_value * fungicide_ef['co2']
                                     + fungicide_value * fungicide_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + fungicide_value * fungicide_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        insecticide_ef = self.get_ef("insecticide")
        insecticide_value = self.crop_protection_data.insecticide_value
        crop_protection_emission += (insecticide_value * insecticide_ef['co2']
                                     + insecticide_value * insecticide_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                                     + insecticide_value * insecticide_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        return crop_protection_emission

    def calculate_energy_emission(self):
        energy_emission = 0

        diesel_ef = self.get_ef("diesel")
        diesel_value = self.energy_data.diesel_value
        energy_emission += (diesel_value * diesel_ef['co2']
                            + diesel_value * diesel_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                            + diesel_value * diesel_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        gasoline_ef = self.get_ef("gasoline")
        gasoline_value = self.energy_data.gasoline_value
        energy_emission += (gasoline_value * gasoline_ef['co2']
                            + gasoline_value * gasoline_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                            + gasoline_value * gasoline_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        electricity_ef = self.get_ef("electricity")
        electricity_value = self.energy_data.electricity_value
        energy_emission += (electricity_value * electricity_ef['co2']
                            + electricity_value * electricity_ef['ch4'] * EmissionCFG.CH4_CONVERSION_VALUE
                            + electricity_value * electricity_ef['n2o'] * EmissionCFG.N2O_CONVERSION_VALUE)

        return energy_emission

    def get_ef(self, name):
        name = name.lower()
        ef_values = self.ef_table.loc[
            self.ef_table['identity_title'].str.lower() == name, ['co2', 'ch4', 'n2o']
        ].squeeze()

        emission_value = ef_values.fillna(0).to_dict()
        logger.info("%s: %s", name, emission_value)
        return emission_value
