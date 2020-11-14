import time
from api.FEMA_House_Dmg_Analytics import *
from api.Air_Quality_Analytics import *
from api.Crime_Analytics import *
from flask import Flask, request
from uszipcode import SearchEngine

app = Flask(__name__)


def get_current_time():
    return {'time': time.time()}


def get_zip_dmg():
    dis_stats = Disaster_Stats()
    zp, state = request.arg['zip'], request.arg['state']
    return {
        'total_dmg_for_zip': dis_stats.get_total_dmg_for_zip(zp),
        'total_dmg_for_state': dis_stats.get_total_dmg_for_state(state),
        'total_dmg': dis_stats.get_total_dmg(),
        'prop_zip_dmg_for_state': dis_stats.get_prop_zip_dmg_for_state(zp, state),
        'prop_zip_dmg_for_nation': dis_stats.get_prop_zip_dmg_for_nation(zp)
    }


def get_air_quality_data():
    aq_stats = Air_Quality_Analytics()
    zp = request.arg['zip']
    search = SearchEngine(simple_zipcode=False)
    city_str = search.by_zipcode(zp).to_dict()['major_city']
    summary_dct = aq_stats.get_local_air_quality_comparison(city_str)
    return summary_dct


def get_crime_analytics_data():
    cr_stats = Crime_Stats()
    # Fill out with state:designation function
    region_dct = {}
    state = request.arg['state']
    region = region_dct['state']
    return {'Top 3 Regional Offenses': cr_stats.get_region_top_three_offense_proportions(region)}
