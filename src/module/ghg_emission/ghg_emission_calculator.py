import pandas as pd
class GHGEmissionCalculator:
    def __init__(self, irrigation_data, organic_amendment_data, land_management_data, crop_protection_data, energy_data):
        self.irrigation_data = irrigation_data
        self.organic_amendment_data = organic_amendment_data
        self.land_management_data = land_management_data
        self.crop_protection_data = crop_protection_data
        self.energy_data = energy_data
        self.emission_factor_table = pd.read_excel('src/module/ghg_emission/emission_table.xlsx')
        print(self.emission_factor_table.head())
    def calculate_emission(self):
        irrigation_emission = self.calculate_irrigation_emission()
        land_management_emission = self.calculate_land_management_emission()
        crop_protection_emission = self.calculate_crop_protection_emission()
        energy_emission = self.calculate_energy_emission()

        total_emission = irrigation_emission + land_management_emission + crop_protection_emission + energy_emission
        return total_emission, irrigation_emission, land_management_emission, crop_protection_emission, energy_emission

    def calculate_irrigation_emission(self):
        irrigation_emission_factor = self.calculate_irrigation_factor()
        print(irrigation_emission_factor)
        days_flooded = self.irrigation_data.days_flooded
        area = self.irrigation_data.area

        irrigation_emission_value = area * irrigation_emission_factor * days_flooded * 25
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

        # print(scaling_factor)
        # print(pow(scaling_factor, 0.59))

        adjusted_irrigation_emission_factor = irrigation_emission_factor * pow(scaling_factor, 0.59)

        return adjusted_irrigation_emission_factor

    def calculate_land_management_emission(self):
        land_management_emission = 0

        fertilizer_emission_factor = self.get_emission_factor(14)
        fertilizer_value = self.land_management_data.fertilizer_value
        land_management_emission += (fertilizer_value * fertilizer_emission_factor['co2']
                                     + fertilizer_value * fertilizer_emission_factor['ch4'] * 25
                                     + fertilizer_value * fertilizer_emission_factor['n2o'] * 298)

        animal_manure_emission_factor = self.get_emission_factor(15)
        animal_manure_value = self.land_management_data.animal_manure_value
        land_management_emission += (animal_manure_value * animal_manure_emission_factor['co2']
                                     + animal_manure_value * animal_manure_emission_factor['ch4'] * 25
                                     + animal_manure_value * animal_manure_emission_factor['n2o'] * 298)

        landfill_emission_factor = self.get_emission_factor(16)
        landfill_value = self.land_management_data.landfill_value
        land_management_emission += (landfill_value * landfill_emission_factor['co2']
                                     + landfill_value * landfill_emission_factor['ch4'] * 25
                                     + landfill_value * landfill_emission_factor['n2o'] * 298)

        incineration_emission_factor = self.get_emission_factor(17)
        incineration_value = self.land_management_data.incineration_value
        land_management_emission += (incineration_value * incineration_emission_factor['co2']
                                     + incineration_value * incineration_emission_factor['ch4'] * 25
                                     + incineration_value * incineration_emission_factor['n2o'] * 298)

        crop_burning_emission_factor = self.get_emission_factor(18)
        crop_burning_value = self.land_management_data.crop_burning_value
        land_management_emission += (crop_burning_value * crop_burning_emission_factor['co2']
                                     + crop_burning_value * crop_burning_emission_factor['ch4'] * 25
                                     + crop_burning_value * crop_burning_emission_factor['n2o'] * 298)

        composting_emission_factor = self.get_emission_factor(19)
        composting_value = self.land_management_data.composting_value
        land_management_emission += (composting_value * composting_emission_factor['co2']
                                     + composting_value * composting_emission_factor['ch4'] * 25
                                     + composting_value * composting_emission_factor['n2o'] * 298)

        return land_management_emission

    def calculate_crop_protection_emission(self):
        crop_protection_emission = 0

        pesticide_emission_factor = self.get_emission_factor(10)
        pesticide_value = self.crop_protection_data.pesticide_value
        crop_protection_emission += (pesticide_value * pesticide_emission_factor['co2']
                                     + pesticide_value * pesticide_emission_factor['ch4'] * 25
                                     + pesticide_value * pesticide_emission_factor['n2o'] * 298)

        herbicide_emission_factor = self.get_emission_factor(11)
        herbicide_value = self.crop_protection_data.herbicide_value
        crop_protection_emission += (herbicide_value * herbicide_emission_factor['co2']
                                     + herbicide_value * herbicide_emission_factor['ch4'] * 25
                                     + herbicide_value * herbicide_emission_factor['n2o'] * 298)

        fungicide_emission_factor = self.get_emission_factor(12)
        fungicide_value = self.crop_protection_data.fungicide_value
        crop_protection_emission += (fungicide_value * fungicide_emission_factor['co2']
                                     + fungicide_value * fungicide_emission_factor['ch4'] * 25
                                     + fungicide_value * fungicide_emission_factor['n2o'] * 298)

        insecticide_emission_factor = self.get_emission_factor(13)
        insecticide_value = self.crop_protection_data.insecticide_value
        crop_protection_emission += (insecticide_value * insecticide_emission_factor['co2']
                                    + insecticide_value * insecticide_emission_factor['ch4'] * 25
                                    + insecticide_value * insecticide_emission_factor['n2o'] * 298)

        return crop_protection_emission

    def calculate_energy_emission(self):
        energy_emission = 0

        diesel_emission_factor = self.get_emission_factor(20)
        diesel_value = self.energy_data.diesel_value
        energy_emission += (diesel_value * diesel_emission_factor['co2']
                            + diesel_value * diesel_emission_factor['ch4'] * 25
                            + diesel_value * diesel_emission_factor['n2o'] * 298)

        gasoline_emission_factor = self.get_emission_factor(21)
        gasoline_value = self.energy_data.gasoline_value
        energy_emission += (gasoline_value * gasoline_emission_factor['co2']
                            + gasoline_value * gasoline_emission_factor['ch4'] * 25
                            + gasoline_value * gasoline_emission_factor['n2o'] * 298)

        electricity_emission_factor = self.get_emission_factor(22)
        electricity_value = self.energy_data.electricity_value
        energy_emission += (electricity_value * electricity_emission_factor['co2']
                            + electricity_value * electricity_emission_factor['ch4'] * 25
                            + electricity_value * electricity_emission_factor['n2o'] * 298)

        return energy_emission

    def get_emission_factor(self, id):
        # print(self.emission_factor_table.iloc[22])
        co2_value = self.emission_factor_table.loc[id]['CO2']
        ch4_value = self.emission_factor_table.loc[id]['CH4']
        n2o_value = self.emission_factor_table.loc[id]['N2O']

        return {'co2': co2_value, 'ch4': ch4_value, 'n2o': n2o_value}