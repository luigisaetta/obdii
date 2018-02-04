"""
#
# Author:       L. Saetta
# created:      27 jan 2018
# last update:  01/02/2018
#
# published under MIT license (see LICENSE file)
"""

# pylint: disable=invalid-name

import configparser
import os
import serial
import sys
import time
import json
from Device import Device

#
# globals
#
# the name of MQTT topic where msgs are sent
TOPIC_GPS = 'owntracks/luigi/googx1'
sleepTime = 5
GPS_FORMAT_STRING = "{0:.6f}"

#
# functions definition
#


def format_float(value):
    return float(GPS_FORMAT_STRING.format(value))

# transforms lat e lon in decimal


def calcola_dec(x):
    DD = int(float(x) / 100)
    SS = float(x) - DD * 100
    Dec = DD + SS / 60
    return Dec

#
# createJSONMsg()
# create the msg in JSON format starting from OBDII readings
#


def createJSONMsg(carID, lat, lon, alt, acc):
    msg = {}

    msg['CARID'] = carID
    msg['lat'] = lat
    msg['lon'] = lon
    msg['alt'] = alt
    msg['acc'] = acc

    # format in JSON
    msgJson = json.dumps(msg)

    return msgJson


#
# Main
#
# read configuration from gateway.ini file
# read OBD2_HOME env variable
OBD2HOME = os.getenv('OBD2_HOME')

config = configparser.ConfigParser()
config.read(OBD2HOME + '/gateway.ini')
carID = config['DEFAULT']['carID']

# clientID is passed to make possible different clientID
# MQTT doesn't allow different clients with same ID (second is disconnected)
gateway = Device("gx2gps")

# init serial
# Here I have used the custom defined name: kpn_gps
ser = serial.Serial('/dev/kpn_gps', 4800, timeout=10)

# try connecting to local MQTT broker in loop
# to handle case in which initially no network connection
while gateway.isConnected() != True:
    try:
        gateway.connect("localhost", 1883, "NO")
    except:
        print('*** Error in MQTT connection !')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])

    time.sleep(sleepTime)

#
# main loop
#
while True:
    gps = ser.readline()

    # print(gps)

    try:
        gps = gps.strip()
        sGps = gps.decode("utf-8")

        # print all NMEA strings with a GPS fix, only if there is a fix (1)

        if sGps.startswith(u'$GPGGA'):
            # print(sGps)
            lat, N, lon, E, F, S, ACC, ALT = sGps.strip().split(u',')[2:10]

            # check if there is a valid GPS fix
            if F == u'2' or F == u'1':
                lat = format_float(calcola_dec(lat))
                lon = format_float(calcola_dec(lon))
                alt = float(ALT)
                acc = float(ACC)

                # print(lat, lon, alt, acc)

                try:
                    # build JSON msg and send to topic on localhost
                    msgJson = createJSONMsg(carID, lat, lon, alt, acc)

                    # msg are published on the local MQTT broker where are read from a NodeRED flow
                    # that publish them in REDIS DB
                    gateway.publish(TOPIC_GPS, msgJson)
                except:
                    print('Error in sending GPS MSG...')
    except:
        # unexpected error ignore and continue
        pass
