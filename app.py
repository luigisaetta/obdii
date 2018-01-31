import mysql.connector as sql
import json as json
import numpy as np
import pandas as pd
import dbconfig as cfg

from flask import Flask
from flask import Response
from flask import request

# globals
HOST = 'mysql'
SOGLIA = 50

app = Flask(__name__)

def format_float(value):
    OBDDATA_FORMAT_STRING = "{0:.2f}"
    return float(OBDDATA_FORMAT_STRING.format(value))

# lista dei trips
@app.route('/car-api/trips')
def find_trips():
    db_connection = sql.connect(host=HOST, database='home1', user=cfg.mysql['user'], password=cfg.mysql['password'])
    
    SQL_SELECT = 'SELECT id, dayhour, start_id, stop_id FROM trips ORDER BY id ASC'

    dfTrips = pd.read_sql(SQL_SELECT, con=db_connection)
    
    vet = []
    
    for index, row in dfTrips.iterrows():
       # single trip
       obj = {}
       obj['ID'] = row['id']
       obj['DAYHOUR'] = row['dayhour']
       obj['START_ID'] = row['start_id'] 
       obj['STOP_ID'] = row['stop_id']

       vet.append(obj)
    
       res = {}
       res['Trips'] = vet

    msg_json = json.dumps(res, sort_keys=True)

    resp = Response(msg_json, status=200, mimetype='application/json')
    return resp

# calcola i dati riassuntivi del trip
@app.route('/car-api/trip')
def calcola_trip():
    db_connection = sql.connect(host=HOST, database='home1', user=cfg.mysql['user'], password=cfg.mysql['password'])
    
    # prepare query
    # DAYHOUR = "27-01-2018 08"
    DAYHOUR = request.args['DAYHOUR']
    # CARID=googx1
    CARID = request.args['CARID']

    SQL_SELECT = 'SELECT id, start_id, stop_id FROM trips WHERE dayhour = "' + DAYHOUR + '"'

    dfTrips = pd.read_sql(SQL_SELECT, con=db_connection)
    
    ID_TRIP = dfTrips['id'][0]
    START_ID = dfTrips['start_id'][0]
    STOP_ID = dfTrips['stop_id'][0]
    
    SQL_SELECT = 'SELECT msg FROM obd2_msg WHERE msg_type = "OBD2" and id > ' + str(START_ID) + ' and id < ' + \
             str(STOP_ID) + ' and carid = "' + CARID + '" order by id ASC'

    dfMesg = pd.read_sql(SQL_SELECT, con=db_connection)
    
    distance = []
    speed = []
    maf = []

    for result in dfMesg['msg']:
        # converte in JSON
        jresult = json.loads(result)
        speed.append(jresult['SPEED'])
        maf.append(jresult['MAF'])
        distance.append(jresult['DISTANCE'])

    df = pd.DataFrame([speed, maf, distance]).T

    # defines column name
    df.columns = ['SPEED', 'MAF', 'DISTANCE']
    
    # calcolo la somma dei valori MAF
    tot_maf = df['MAF'].sum()
    # intervallo tra i punti
    delta_time = 7
    # uso rapporto ideale (14.7)
    tot_aria = delta_time * tot_maf
    # gasolio in grammi
    tot_gasolio = tot_aria / 14.7
    tot_litri_gasolio = tot_gasolio/840
    tot_litri_gasolio = format_float(tot_litri_gasolio)

    # distanza
    ini_dist = df['DISTANCE'].iloc[0]
    end_dist = df['DISTANCE'].iloc[-1]
    trip_len = (end_dist - ini_dist)

    # calcola num_punti speed > SOGLIA
    over = df['SPEED'] > SOGLIA
    count_over = sum(over)    
    points = len(over)
    ratio = (count_over/points)*100
    
    v_result = {}
    v_result['ID'] = str(ID_TRIP) 
    v_result['GASOLINE'] = tot_litri_gasolio
    v_result['DISTANCE'] = trip_len
    v_result['SPEED_OVER_THRESHOLD'] = format_float(ratio)

    msg_json = json.dumps(v_result)

    resp = Response(msg_json, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
