import time
from FEMA_House_Dmg_Analytics import *
from Air_Quality_Analytics import *
from Crime_Analytics import *
from flask import Flask, request
from uszipcode import SearchEngine

app = Flask(__name__)


@app.route('/data')
def get_data():
    zip, state = request.args['zip'], request.args['state']
    result = {}
    result.update(get_zip_dmg(zip, state))
    result.update(get_crime_analytics_data(state))
    # result.update(get_air_quality_data(zip))
    return result


def get_zip_dmg(zp, state):
    dis_stats = Disaster_Stats()
    return {
        'total_dmg_for_zip': dis_stats.get_total_dmg_for_zip(zp),
        'total_dmg_for_state': dis_stats.get_total_dmg_for_state(state),
        'total_dmg': dis_stats.get_total_dmg(),
        'prop_zip_dmg_for_state': dis_stats.get_prop_zip_dmg_for_state(zp, state),
        'prop_zip_dmg_for_nation': dis_stats.get_prop_zip_dmg_for_nation(zp)
    }


def get_air_quality_data(zp, city=""):
    aq_stats = Air_Quality_Analytics()
    city_str = city
    if len(city) > 0:
        search = SearchEngine(simple_zipcode=False)
        city_str = search.by_zipcode(zp).to_dict()['major_city']
    summary_dct = aq_stats.get_local_air_quality_comparison(city_str)
    return summary_dct


def get_crime_analytics_data(state):
    cr_stats = Crime_Stats()
    # Fill out with state:designation function
    region_dct = {'OH': 'Midwest'}
    region = region_dct[state]
    return {'top_regional_offenses': cr_stats.get_region_top_three_offense_proportions(region)}
