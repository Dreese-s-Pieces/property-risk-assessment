import pandas as pd
from scipy.stats import t
import numpy as np
import requests


def make_dataframe(r):
    """Extracts data from request r and returns a DataFrame."""
    rows = []
    for item in r.json()['data']:
        rows.append([item['lat'], item['lon'], item['aqi'], item['station']['name']])
    df = pd.DataFrame(rows, columns=['lat', 'lon', 'aqi', 'name'])
    df['aqi'] = pd.to_numeric(df.aqi, errors='coerce')
    return df


def one_samp_t_test(df, city_str):
    return (df[df['name'].split(",")[0] == city_str]['aqi'] - df['aqi'].mean()) / (
        df['aqi'].var() / df.count()) ** (1 / 2)


def get_request_data(url):
    return requests.get(url).json()


class Air_Quality_Analytics():
    def __init__(self):
        self.city_str = ""
        self.url = "https://api.waqi.info/feed/" + self.city_str + "/?token=fe269bc83b983ff958090f5808afa12eed57f14f"

    def get_local_air_quality_comparison(self, city_str):
        self.city_str = city_str
        req_data = self.get_request_data(self.url)
        local_df = make_dataframe(req_data)
        air_quality_comp = dict()
        air_quality_comp['Deviation of AQI From Closest Cities'] = local_df[local_df['name'].split(',')[0] == city_str][
                                                                       'aqi'].sum() - local_df[
                                                                       'aqi'].sum() / local_df.count()
        air_quality_comp[
            'Probability of AQI Being Significantly Different From Surrounding Cities'] = self.one_samp_t_test(
            local_df[local_df['name'].split(',')[0] != city_str], self.city_str)
        air_quality_comp['Probability of AQI Being Significantly Different From Surrounding Cities'] = t.sf(
            np.abs(air_quality_comp['Probability of AQI Being Significantly Different From Surrounding Cities']),
            local_df.count() - 1)

        return air_quality_comp

    def get_air_quality_index(self, city_str):
        self.city_str = city_str
        return self.get_request_data(self.url)["data"]["aqi"]
