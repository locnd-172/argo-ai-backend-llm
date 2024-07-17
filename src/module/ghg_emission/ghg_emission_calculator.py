import pandas as pd
class GHGEmissionCalculator:
    def __init__(self, irrigation_data, land_management_data, crop_protection_data, energy_data):
        self.irrigation_data = irrigation_data
        self.land_management_data = land_management_data
        self.crop_protection_data = crop_protection_data
        self.energy_data = energy_data
        self.emission_factor_table = pd.read_excel('src/module/ghg_emission/emission_table.xlsx')
        print(self.emission_factor_table.head())
    def calculate_emission(self):
        irrigation_emission = 0
        land_management_emission = 0
        crop_protection_emission = 0
        energy_emission = self.calculate_energy_emission()

        total_emission = irrigation_emission + land_management_emission + crop_protection_emission + energy_emission
        return total_emission

    def calculate_irrigation_emission(self):
        return 0

    def calculate_land_management_emission(self):
        return 0

    def calculate_crop_protection_emission(self):
        for crop_protection in self.crop_protection_data:
            a = 0
        return 0

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