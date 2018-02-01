import json as json

import mysql.connector as sql
import numpy as np
import pandas as pd
import sys
from flask import Flask, Response, request

import dbconfig as cfg

# globals
HOST = 'mysql'
DATABASE = 'home1'
# THRESHOLD for SPEED
SOGLIA = 50
FLOAT_FORMAT_STRING = "{0:.2f}"

app = Flask(__name__)


def format_float(value):
    return float(FLOAT_FORMAT_STRING.format(value))

#
# list of the trips
#


@app.route('/car-api/trips')
def find_trips():
    db_connection = sql.connect(
        host=HOST, database=DATABASE, user=cfg.mysql['user'], password=cfg.mysql['password'])

    SQL_SELECT = 'SELECT id, dayhour, start_id, stop_id FROM trips ORDER BY id ASC'

    # load data in Dataframe
    dfTrips = pd.read_sql(SQL_SELECT, con=db_connection)

    # vector for the list of trips
    vet = []

    for index, row in dfTrips.iterrows():
        # single trip
        obj = {}
        obj['ID'] = row['id']
        obj['DAYHOUR'] = row['dayhour']
        obj['START_ID'] = row['start_id']
        obj['STOP_ID'] = row['stop_id']

        vet.append(obj)

    # build the response object
    res = {}
    res['TRIPS'] = vet

    msg_json = json.dumps(res, sort_keys=True)

    resp = Response(msg_json, status=200, mimetype='application/json')
    return resp

#
# calculate TRIP summry data (consumption, distance, speed_over_threshold)
#


@app.route('/car-api/trip/findByDayHour')
def calcola_trip():
    try:
        db_connection = sql.connect(
            host=HOST, database=DATABASE, user=cfg.mysql['user'], password=cfg.mysql['password'])

        # prepare query
        # DAYHOUR = "27-01-2018 08"
        # TODO: should control presence of parms...
        DAYHOUR = request.args['DAYHOUR']
        # CARID=googx1
        CARID = request.args['CARID']

        # identify TRIP from DAYHOUR and CARID
        SQL_SELECT = 'SELECT id, start_id, stop_id FROM trips WHERE dayhour = "' + DAYHOUR + '"'

        dfTrips = pd.read_sql(SQL_SELECT, con=db_connection)

        ID_TRIP = dfTrips['id'][0]
        START_ID = dfTrips['start_id'][0]
        STOP_ID = dfTrips['stop_id'][0]

        # READ msgs from TRIP into DataFrame
        SQL_SELECT = 'SELECT msg FROM obd2_msg WHERE msg_type = "OBD2" and id > ' + str(START_ID) + ' and id < ' + \
            str(STOP_ID) + ' and carid = "' + CARID + '" order by id ASC'

        dfMesg = pd.read_sql(SQL_SELECT, con=db_connection)

        distance = []
        speed = []
        maf = []

        for result in dfMesg['msg']:
            # converts in JSON
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
        tot_litri_gasolio = tot_gasolio / 840
        tot_litri_gasolio = format_float(tot_litri_gasolio)

        # total distance calculated as end-start
        ini_dist = df['DISTANCE'].iloc[0]
        end_dist = df['DISTANCE'].iloc[-1]
        trip_len = (end_dist - ini_dist)

        # calculate num_punti speed > SOGLIA
        over = df['SPEED'] > SOGLIA
        count_over = sum(over)
        points = len(over)
        ratio = (count_over / points) * 100

        v_result = {}
        v_result['ID'] = str(ID_TRIP)
        v_result['GASOLINE'] = tot_litri_gasolio
        v_result['DISTANCE'] = trip_len

        # SPEED_OVER_THRESHOLD can be considered as an indicator of how much
        # the driver is taking risks
        v_result['SPEED_OVER_THRESHOLD'] = format_float(ratio)

        msg_json = json.dumps(v_result)

        resp = Response(msg_json, status=200, mimetype='application/json')

        return resp

    except:
        errore = {}
        errore['CODE'] = -1
        errore['MESSAGE'] = 'Error in GET TRIPS'

        return errore


@app.route('/car-api/trip/<ID>')
def find_trip_by_id(ID):
    try:
        db_connection = sql.connect(
            host=HOST, database=DATABASE, user=cfg.mysql['user'], password=cfg.mysql['password'])

        # prepare query

        # TODO: should control presence of parms...
        # ID = request.args['ID']

        # identify TRIP from DAYHOUR and CARID
        SQL_SELECT = 'SELECT start_id, stop_id FROM trips WHERE id = "' + \
            str(ID) + '"'

        dfTrips = pd.read_sql(SQL_SELECT, con=db_connection)

        START_ID = dfTrips['start_id'][0]
        STOP_ID = dfTrips['stop_id'][0]

        # READ msgs from TRIP into DataFrame
        SQL_SELECT = 'SELECT msg FROM obd2_msg WHERE msg_type = "OBD2" and id > ' + str(START_ID) + ' and id < ' + \
            str(STOP_ID) + ' order by id ASC'

        dfMesg = pd.read_sql(SQL_SELECT, con=db_connection)

        vet = []

        for msg in dfMesg['msg']:
            # converts in JSON
            vet.append(msg)

        v_result = {}
        v_result['MSG'] = vet

        msg_json = json.dumps(v_result)

        resp = Response(msg_json, status=200, mimetype='application/json')

        return resp

    except:
        print('\n')
        print('*** Error in parsing command: ')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])

        errore = {}
        errore['CODE'] = -1
        errore['MESSAGE'] = 'Error in GET TRIPS'

        return errore

#
# list of the cars
#


@app.route('/car-api/cars')
def find_cars():
    db_connection = sql.connect(
        host=HOST, database=DATABASE, user=cfg.mysql['user'], password=cfg.mysql['password'])

    SQL_SELECT = 'SELECT id, carid FROM cars ORDER BY id ASC'

    # load data in Dataframe
    dfCars = pd.read_sql(SQL_SELECT, con=db_connection)

    # vector for the list of cars
    vet = []

    for index, row in dfCars.iterrows():
        # single trip
        obj = {}
        obj['ID'] = row['id']
        obj['CARID'] = row['carid']
        # obj['NOTES'] = row[notes]

        vet.append(obj)

    # build the response object
    res = {}
    res['CARS'] = vet

    msg_json = json.dumps(res, sort_keys=True)

    resp = Response(msg_json, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
