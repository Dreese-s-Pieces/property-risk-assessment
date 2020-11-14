import time
import FEMA_House_Dmg_Analytics as fema
from flask import Flask, request

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/disaster')
def get_zip_dmg():
    dis_stats = fema.Disaster_Stats()
    return {
            'total_dmg_for_zip': dis_stats.get_total_dmg_for_zip(request.arg['zip']),
            'total_dmg_for_state': dis_stats.get_total_dmg_for_state(request.arg['state']),
            'total_dmg': dis_stats.get_total_dmg(),
            'prop_zip_dmg_for_state': dis_stats.get_prop_zip_dmg_for_state(request.arg['zip'], request.arg['state']),
            'prop_zip_dmg_for_nation': dis_stats.get_prop_zip_dmg_for_nation(request.arg['zip']) 
           }

# @app.route('/disaster/state_level_disasters')
# def get_state_level_disasters():
#     dis_stats = fema.Disaster_Stats()
#     print(request.args['state'])
#     return {'state_level_disasters': dis_stats.get_state_national_proportion_of_certain_disaster(request.args['disaster'], request.args['state'])}
