import pandas as pd
import asyncio

from src.config.constant import EmissionCFG
from src.module.ghg_emission.emission_factors_services import get_all_emission_factors


class GHGEmissionCalculator:
    def __init__(self, irrigation_data, organic_amendment_data, land_management_data, crop_protection_data,
                 energy_data):
        self.irrigation_data = irrigation_data
        self.organic_amendment_data = organic_amendment_data
        self.land_management_data = land_management_data
        self.crop_protection_data = crop_protection_data
        self.energy_data = energy_data
        self.CH4_VALUE = EmissionCFG.CH4_CONVERSION_VALUE
        self.N2O_VALUE = EmissionCFG.N2O_CONVERSION_VALUE
        self.SCALING_FACTOR_VALUE = EmissionCFG.SCALING_FACTOR_VALUE
        self.emission_factor_table = self.get_emission_factor_table()

    def get_emission_factor_table(self):
        emission_factor_table = asyncio.run(get_all_emission_factors())
        emission_factor_table = emission_factor_table[1:]
        emission_factor_table = emission_factor_table[::-1]
        emission_factor_table = pd.DataFrame(emission_factor_table)
        return emission_factor_table

    def calculate_emission(self):
        irrigation_emission = self.calculate_irrigation_emission()
        land_management_emission = self.calculate_land_management_emission()
        crop_protection_emission = self.calculate_crop_protection_emission()
        energy_emission = self.calculate_energy_emission()

        total_emission = irrigation_emission + land_management_emission + crop_protection_emission + energy_emission
        return total_emission, irrigation_emission, land_management_emission, crop_protection_emission, energy_emission

    def calculate_irrigation_emission(self):
        irrigation_emission_factor = self.calculate_irrigation_factor()
        days_flooded = self.irrigation_data.days_flooded
        area = self.irrigation_data.area

        irrigation_emission_value = area * irrigation_emission_factor * days_flooded * self.CH4_VALUE
        return irrigation_emission_value

    def calculate_irrigation_factor(self):
        irrigation_emission_factor = 0
        if self.irrigation_data.is_continuous_flooding:
            irrigation_emission_factor = self.get_emission_factor(0)
        elif self.irrigation_data.is_single_aeration:
            irrigation_emission_factor = self.get_emission_factor(1)
        elif self.irrigation_data.is_multiple_aeration:
            irrigation_emission_factor = self.get_emission_factor(2)
        elif self.irrigation_data.is_rainfed:
            irrigation_emission_factor = self.get_emission_factor(3)
        elif self.irrigation_data.is_upland:
            irrigation_emission_factor = self.get_emission_factor(4)
        irrigation_emission_factor = irrigation_emission_factor['ch4']

        scaling_factor = 1
        straw_incorporated_short_emission_factor = self.get_emission_factor(5)['ch4']
        straw_incorporated_short_value = self.organic_amendment_data.straw_incorporated_short_value
        scaling_factor += straw_incorporated_short_value * straw_incorporated_short_emission_factor

        straw_incorporated_long_emission_factor = self.get_emission_factor(6)['ch4']
        straw_incorporated_long_value = self.organic_amendment_data.straw_incorporated_long_value
        scaling_factor += straw_incorporated_long_value * straw_incorporated_long_emission_factor

        compost_emission_factor = self.get_emission_factor(7)['ch4']
        compost_value = self.organic_amendment_data.compost_value
        scaling_factor += compost_value * compost_emission_factor

        farm_yard_manure_emission_factor = self.get_emission_factor(8)['ch4']
        farm_yard_manure_value = self.organic_amendment_data.farm_yard_manure_value
        scaling_factor += farm_yard_manure_value * farm_yard_manure_emission_factor

        green_manure_emission_factor = self.get_emission_factor(9)['ch4']
        green_manure_value = self.organic_amendment_data.green_manure_value
        scaling_factor += green_manure_value * green_manure_emission_factor

        adjusted_irrigation_emission_factor = irrigation_emission_factor * pow(scaling_factor, self.SCALING_FACTOR_VALUE)

        return adjusted_irrigation_emission_factor

    def calculate_land_management_emission(self):
        land_management_emission = 0

        fertilizer_emission_factor = self.get_emission_factor(14)
        fertilizer_value = self.land_management_data.fertilizer_value
        land_management_emission += (fertilizer_value * fertilizer_emission_factor['co2']
                                     + fertilizer_value * fertilizer_emission_factor['ch4'] * self.CH4_VALUE
                                     + fertilizer_value * fertilizer_emission_factor['n2o'] * self.N2O_VALUE)

        animal_manure_emission_factor = self.get_emission_factor(15)
        animal_manure_value = self.land_management_data.animal_manure_value
        land_management_emission += (animal_manure_value * animal_manure_emission_factor['co2']
                                     + animal_manure_value * animal_manure_emission_factor['ch4'] * self.CH4_VALUE
                                     + animal_manure_value * animal_manure_emission_factor['n2o'] * self.N2O_VALUE)

        landfill_emission_factor = self.get_emission_factor(16)
        landfill_value = self.land_management_data.landfill_value
        land_management_emission += (landfill_value * landfill_emission_factor['co2']
                                     + landfill_value * landfill_emission_factor['ch4'] * self.CH4_VALUE
                                     + landfill_value * landfill_emission_factor['n2o'] * self.N2O_VALUE)

        incineration_emission_factor = self.get_emission_factor(17)
        incineration_value = self.land_management_data.incineration_value
        land_management_emission += (incineration_value * incineration_emission_factor['co2']
                                     + incineration_value * incineration_emission_factor['ch4'] * self.CH4_VALUE
                                     + incineration_value * incineration_emission_factor['n2o'] * self.N2O_VALUE)

        crop_burning_emission_factor = self.get_emission_factor(18)
        crop_burning_value = self.land_management_data.crop_burning_value
        land_management_emission += (crop_burning_value * crop_burning_emission_factor['co2']
                                     + crop_burning_value * crop_burning_emission_factor['ch4'] * self.CH4_VALUE
                                     + crop_burning_value * crop_burning_emission_factor['n2o'] * self.N2O_VALUE)

        composting_emission_factor = self.get_emission_factor(19)
        composting_value = self.land_management_data.composting_value
        land_management_emission += (composting_value * composting_emission_factor['co2']
                                     + composting_value * composting_emission_factor['ch4'] * self.CH4_VALUE
                                     + composting_value * composting_emission_factor['n2o'] * self.N2O_VALUE)

        return land_management_emission

    def calculate_crop_protection_emission(self):
        crop_protection_emission = 0

        pesticide_emission_factor = self.get_emission_factor(10)
        pesticide_value = self.crop_protection_data.pesticide_value
        crop_protection_emission += (pesticide_value * pesticide_emission_factor['co2']
                                     + pesticide_value * pesticide_emission_factor['ch4'] * self.CH4_VALUE
                                     + pesticide_value * pesticide_emission_factor['n2o'] * self.N2O_VALUE)

        herbicide_emission_factor = self.get_emission_factor(11)
        herbicide_value = self.crop_protection_data.herbicide_value
        crop_protection_emission += (herbicide_value * herbicide_emission_factor['co2']
                                     + herbicide_value * herbicide_emission_factor['ch4'] * self.CH4_VALUE
                                     + herbicide_value * herbicide_emission_factor['n2o'] * self.N2O_VALUE)

        fungicide_emission_factor = self.get_emission_factor(12)
        fungicide_value = self.crop_protection_data.fungicide_value
        crop_protection_emission += (fungicide_value * fungicide_emission_factor['co2']
                                     + fungicide_value * fungicide_emission_factor['ch4'] * self.CH4_VALUE
                                     + fungicide_value * fungicide_emission_factor['n2o'] * self.N2O_VALUE)

        insecticide_emission_factor = self.get_emission_factor(13)
        insecticide_value = self.crop_protection_data.insecticide_value
        crop_protection_emission += (insecticide_value * insecticide_emission_factor['co2']
                                     + insecticide_value * insecticide_emission_factor['ch4'] * self.CH4_VALUE
                                     + insecticide_value * insecticide_emission_factor['n2o'] * self.N2O_VALUE)

        return crop_protection_emission

    def calculate_energy_emission(self):
        energy_emission = 0

        diesel_emission_factor = self.get_emission_factor(20)
        diesel_value = self.energy_data.diesel_value
        energy_emission += (diesel_value * diesel_emission_factor['co2']
                            + diesel_value * diesel_emission_factor['ch4'] * self.CH4_VALUE
                            + diesel_value * diesel_emission_factor['n2o'] * self.N2O_VALUE)

        gasoline_emission_factor = self.get_emission_factor(21)
        gasoline_value = self.energy_data.gasoline_value
        energy_emission += (gasoline_value * gasoline_emission_factor['co2']
                            + gasoline_value * gasoline_emission_factor['ch4'] * self.CH4_VALUE
                            + gasoline_value * gasoline_emission_factor['n2o'] * self.N2O_VALUE)

        electricity_emission_factor = self.get_emission_factor(22)
        electricity_value = self.energy_data.electricity_value
        energy_emission += (electricity_value * electricity_emission_factor['co2']
                            + electricity_value * electricity_emission_factor['ch4'] * self.CH4_VALUE
                            + electricity_value * electricity_emission_factor['n2o'] * self.N2O_VALUE)

        return energy_emission

    def get_emission_factor(self, id):
        co2_value = self.emission_factor_table.loc[id]['co2']
        ch4_value = self.emission_factor_table.loc[id]['ch4']
        n2o_value = self.emission_factor_table.loc[id]['n2o']

        return {'co2': co2_value, 'ch4': ch4_value, 'n2o': n2o_value}
