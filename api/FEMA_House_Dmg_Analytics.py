import pandas as pd

class Disaster_Stats():
    def __init__(self, fp):
        self.disasters_csv = pd.read_csv(fp)

    def get_state_level_disasters(self, state_str):
        return self.disasters_csv[self.disasters_csv['state'] == state_str]

    def get_state_national_proportion_of_certain_disaster(self, disaster, state_str):
        state_csv = self.disasters_csv.get_state_level_get_state_level_disasters(state_str)
        state_csv = state_csv[state_csv['declarationTitle'] == disaster]
        nat_csv = self.disasters_csv[self.disasters_csv['declarationTitle'] == disaster]
        return state_csv.count()/nat_csv.count()

    def get_total_dmg_for_zip(self, zip_str):
        return self.disasters_csv[self.disasters_csv['zipCode'] == zip_str]['averageFemaInspectedDamage'].sum()

    def get_total_dmg_for_state(self, state_str):
        return self.disasters_csv[self.disasters_csv['state'] == state_str]['averageFemaInspectedDamage'].sum()

    def get_total_dmg(self):
        return self.disasters_csv['averageFemaInspectedDamage'].sum()

    def get_prop_zip_dmg_for_state(self, zip_str,state_str):
        return self.disasters_csv.get_total_dmg_for_zip(zip_str)/self.disasters_csv.get_total_dmg_for_state(state_str)

    def get_prop_zip_dmg_for_nation(self, zip_str):
        return self.disasters_csv.get_total_dmg_for_zip(zip_str)/self.disasters_csv.get_total_dmg()