import time
import FEMA_House_Dmg_Analytics as fema
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/disaster')
def get_zip_dmg():
    dis_stats = fema.Disaster_Stats()
    return jsonify({
            'total_dmg_for_zip': dis_stats.get_total_dmg_for_zip(request.args['zip']),
            'total_dmg_for_state': dis_stats.get_total_dmg_for_state(request.args['state']),
            'total_dmg': dis_stats.get_total_dmg(),
            'prop_zip_dmg_for_state': dis_stats.get_prop_zip_dmg_for_state(request.args['zip'], request.args['state']),
            'prop_zip_dmg_for_nation': dis_stats.get_prop_zip_dmg_for_nation(request.args['zip']) 
           })
