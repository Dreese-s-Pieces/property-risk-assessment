import pandas as pd
import numpy as np
import requests
from numpy.core._multiarray_umath import ndarray
from sklearn.linear_model import LinearRegression
import numpy as np
from uszipcode import SearchEngine


class Disaster_Stats():
    reg_coef: ndarray

    def __init__(self, url="https://www.fema.gov/api/open/v2/HousingAssistanceOwners"):
        self.disasters_csv = requests.get(url).json()
        self.disasters_csv = pd.DataFrame.from_dict(self.disasters_csv["HousingAssistanceOwners"])
        self.reg_coef = np.asarray([])
        self.reg_intercept = 0

    def get_state_level_disasters(self, state_str):
        print(self.disasters_csv[self.disasters_csv['state'] == state_str])
        return self.disasters_csv[self.disasters_csv['state'] == state_str]

    # Needs changes, declarationTitle not present in V2
    def get_state_national_proportion_of_certain_disaster(self, disaster, state_str):
        state_csv = self.get_state_level_disasters(state_str)
        print(state_csv)
        state_csv = state_csv[state_csv['declarationTitle'] == disaster]
        nat_csv = self.disasters_csv[self.disasters_csv['declarationTitle'] == disaster]
        return state_csv.count() / nat_csv.count()

    def get_total_dmg_for_zip(self, zip_str):
        result = self.disasters_csv[self.disasters_csv['zipCode'] == zip_str]['averageFemaInspectedDamage'].sum()
        if np.isnan(result):
            return 0

        return result

    def get_total_dmg_for_state(self, state_str):
        result = self.disasters_csv[self.disasters_csv['state'] == state_str]['averageFemaInspectedDamage'].sum()
        if np.isnan(result):
            return 0

        return result

    def get_total_dmg(self):
        result = self.disasters_csv['averageFemaInspectedDamage'].sum()
        if np.isnan(result):
            return 0

        return result

    def get_prop_zip_dmg_for_state(self, zip_str, state_str):
        result = self.get_total_dmg_for_zip(zip_str) / self.get_total_dmg_for_state(state_str)
        if np.isnan(result):
            return 0

        return result

    def get_prop_zip_dmg_for_state(self, zip_str, state_str):
        result = self.get_total_dmg_for_zip(zip_str) / self.get_total_dmg_for_state(state_str)
        if np.isnan(result):
            return 0

        return result

    def get_prop_zip_dmg_for_nation(self, zip_str):
        result = self.get_total_dmg_for_zip(zip_str) / self.get_total_dmg()
        if np.isnan(result):
            return 0

        return result

    def train(self):
        X_train = self.disasters_csv.loc[:, self.disasters_csv.columns != 'averageFemaInspectedDamage']
        search = SearchEngine(simple_zipcode=False)
        train_dct = {'median_home_value': [], 'zip_code': [], 'population_density': []}
        X_train = X_train.dropna()
        for index, row in X_train.iterrows():
            zp = row['zipCode']
            zip_dct = search.by_zipcode(zp).to_dict()
            train_dct['median_home_value'].append(zip_dct['median_home_value'])
            train_dct['zip_code'] = zp
            train_dct['population_density'].append(zip_dct['population_density'])
        reg = LinearRegression().fit(pd.DataFrame(train_dct).fillna(method='bfill'),
                                     self.disasters_csv['averageFemaInspectedDamage'])
        self.reg_coef = reg.coef_
        self.reg_intercept = reg.intercept_

    def inference(self, zip_code, population_density=0, median_home_value=0):
        zp = int(zip_code)
        print(zp)
        if population_density + median_home_value == 0:
            search = SearchEngine(simple_zipcode=False)
            zip_dct = search.by_zipcode(zp).to_dict()
            population_density = zip_dct['population_density']
            median_home_value = zip_dct['median_home_value']
        inp = np.asarray([median_home_value, zip_code, population_density])
        result = 0
        try:
            result = np.dot(self.reg_coef, inp) + self.reg_intercept
            print(result)
        except:
            print('failed')
        print(result)
        return result

# ds_stats = Disaster_Stats()
# ds_stats.train()
# print(ds_stats.inference(zip_code=43201))
