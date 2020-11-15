import time
from FEMA_House_Dmg_Analytics import *
from Air_Quality_Analytics import *
from Crime_Analytics import *
from flask import Flask, request
from uszipcode import SearchEngine

app = Flask(__name__)

northeast = {'PA', 'NY', 'NJ', 'VT', 'NH', 'MA', 'CT', 'RI', 'ME'}
midwest = {'ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'MI', 'IL', 'IN', 'OH'}
south = {'TX', 'OK', 'AR', 'LA', 'MS', 'AL', 'TN', 'KY', 'FL', 'GA', 'SC', 'NC', 'VA', 'WV', 'MD', 'DE'}
west = {'WA', 'OR', 'CA', 'AK', 'HI', 'ID', 'MT', 'WY', 'NV', 'UT', 'CO', 'AZ', 'NM'}

@app.route('/data')
def get_data():
    zip, state, city= request.args['zip'], request.args['state'], request.args['city']
    if state in northeast:
        region = 'Northeast'
    elif state in midwest:
        region = 'Midwest'
    elif state in south:
        region = 'South'
    else:
        region = 'West'

    result = { 'region': region }
    result.update(get_zip_dmg(zip, state))


    try:
        result.update(get_crime_analytics_data(region))
    except:
        pass

    try:
        result.update(get_air_quality_data(zip, city))
    except:
        pass

    print(result)

    return result


def get_zip_dmg(zp, state):
    dis_stats = Disaster_Stats()
    dis_stats.train()
    return {
        'total_dmg_for_zip': dis_stats.get_total_dmg_for_zip(zp),
        'total_dmg_for_state': dis_stats.get_total_dmg_for_state(state),
        'total_dmg': dis_stats.get_total_dmg(),
        'prop_zip_dmg_for_state': dis_stats.get_prop_zip_dmg_for_state(zp, state),
        'prop_zip_dmg_for_nation': dis_stats.get_prop_zip_dmg_for_nation(zp)
        # 'predicted_zip_dmg': dis_stats.inference(zp)
    }


def get_air_quality_data(zp, city=""):
    aq_stats = Air_Quality_Analytics()
    city_str = city
    if len(city) > 0:
        search = SearchEngine(simple_zipcode=False)
        city_str = search.by_zipcode(zp).to_dict()['major_city']
    summary_dct = aq_stats.get_local_air_quality_comparison(city_str)
    return summary_dct


def get_crime_analytics_data(region):
    cr_stats = Crime_Stats()
    return {'top_regional_offenses': cr_stats.get_region_top_three_offense_proportions(region)}
