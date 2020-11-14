import time
from api import FEMA_House_Dmg_Analytics as fema
from flask import Flask

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}
