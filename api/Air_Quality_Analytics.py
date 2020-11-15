import pandas as pd
from scipy.stats import t
import numpy as np
import requests


def make_dataframe(r):
    rows = []
    for item in r['data']:
        rows.append([item['lat'], item['lon'], item['aqi'], item['station']['name']])
    df = pd.DataFrame(rows, columns=['lat', 'lon', 'aqi', 'name'])
    df['aqi'] = pd.to_numeric(df.aqi, errors='coerce')
    return df


def one_samp_t_test(df, diff):
    return diff / (
        df['aqi'].var() / df.count()) ** (1 / 2)


def get_request_data(url):
    return requests.get(url).json()


class Air_Quality_Analytics():
    def __init__(self):
        self.base_url = "https://api.waqi.info/feed/"
        self.city_str = ""
        self.url = self.base_url + self.city_str + "/?token=fe269bc83b983ff958090f5808afa12eed57f14f"

    def get_local_air_quality_comparison(self, city_str, tolerance=2.0):
        self.city_str = city_str
        token = "fe269bc83b983ff958090f5808afa12eed57f14f"
        req_data = get_request_data(self.base_url + self.city_str + "/?token=" + token)

        lat, lng = req_data['data']['city']['geo']

        latlngbx = str(lat) + "," + str(lng) + "," + str(lat + tolerance) + "," + str(lng + tolerance)
        r = requests.get("https://api.waqi.info/" + f"/map/bounds/?latlng={latlngbx}&token={token}").json()
        if len(r['data']) > 0:
            local_df = make_dataframe(r)
            air_quality_comp = {
                'deviation': 'Not found',
                'probability': 'Not found'
            }

            deviation = local_df[local_df['name'].str.contains(city_str)]['aqi'].mean() - local_df['aqi'].mean()

            if not np.isnan(deviation):
                air_quality_comp['deviation'] = deviation

            probability = one_samp_t_test(local_df[local_df['name'].str.contains(city_str)], deviation)
            probability = t.sf(np.abs(probability), local_df.count() - 1)[0]

            if not np.isnan(probability):
                air_quality_comp['probability'] = probability

            return air_quality_comp

    def get_air_quality_index(self, city_str):
        self.city_str = city_str
        try:
            return get_request_data(self.base_url + self.city_str + "/?token=fe269bc83b983ff958090f5808afa12eed57f14f")['data']["aqi"]
        except:
            pass

# AQA = Air_Quality_Analytics()
# print(AQA.get_local_air_quality_comparison('Los Angeles'))

