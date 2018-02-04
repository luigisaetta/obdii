"""
#
# Author:       L. Saetta
# created:      27 december 2017
# last update:  21/01/2018
#
# published under MIT license (see LICENSE file)
"""

# pylint: disable=invalid-name

import configparser
import datetime
import json
import os
import requests
import sys
import time

# only if using Googe Voice
sys.path.append('/home/pi/AIY-voice-kit-python/src')
import aiy.voicehat


from Device import Device
from OBDII import OBDII
from OBDIISimulator import OBDIISimulator

# control Python Version
vers = sys.version_info.major

# Configuration
#  to format datetime
STFORMAT1 = "%d-%m-%Y %H:%M:%S"
STFORMAT2 = "%d-%m-%Y"
# used for START_TRIP msg
STFORMAT3 = "%d-%m-%Y %H"

# send a msg every 5 sec.
sleepTime = 5
# the name of MQTT topic where msgs are sent
TOPIC_NAME = 'cardata'
TOPIC_ALERTS_NAME = "caralerts"

# read configuration from gateway.ini file
# read OBD2_HOME env variable
OBD2HOME = os.getenv('OBD2_HOME')

config = configparser.ConfigParser()
config.read(OBD2HOME + '/gateway.ini')
msgLogging = config['DEFAULT']['msgLogging']
carID = config['DEFAULT']['carID']

# should be read from config file
HOST = "ubuntucontainers-dashboariotnew-zekci6cs.srv.ravcloud.com"
PORT = 8883

# file name for local logging
FNAME = OBD2HOME + "/msgs" + datetime.datetime.now().strftime(STFORMAT2) + ".log"

#
# get Position
#


def get_position():
    URL_POSITION = 'http://localhost:1880/position'

    lat = 0
    lon = 0
    alt = 0

    try:
        response = requests.get(URL_POSITION)

        jData = json.loads(response.content.decode("utf-8"))

        lat = jData['lat']
        lon = jData['lon']
        alt = jData['alt']
    except:
        print('Error in GET position')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])

    # if error returns zeros
    return lat, lon, alt

#
# createJSONMsg()
# create the msg in JSON format starting from OBDII readings
#


def createJSONMsg():
    msg = {}

    # in the main code it is defined if Simulator or not !
    msg = obdii.getMessage()
    msg['CARID'] = carID

    # added 21/01/2018 (Sensor Fusion)
    # get Position and add to msg
    lat, lon, alt = get_position()

    msg['LAT'] = lat
    msg['LON'] = lon
    msg['ALT'] = alt

    # format in JSON
    msgJson = json.dumps(msg)

    return msgJson

#
#
# createEventMsg
#


def createEventMsg(event_type):
    msg = {}

    # in the main code it is defined if Simulator or not !
    msg['EVENT_TYPE'] = event_type
    msg['CARID'] = carID
    msg['DAYHOUR'] = datetime.datetime.now().strftime(STFORMAT3)

    # format in JSON
    msgJson = json.dumps(msg)

    return msgJson

#
# **** Main ****
#


#
# Test if simulation mode (no acquiring data from OBDII)
#
# runMode = SIMUL|ACQUIRE|NULL (null means ACQUIRE)
parLenght = len(sys.argv)

if parLenght >= 2:
    runMode = sys.argv[1]
else:
    runMode = "ACQUIRE"

print("")
print("***")
print("*** OBD2 Data Acquisition Program started ***")
print("***")
print("*** RUN MODE: ", runMode)
print('*** Python Version ', vers)

# MQTT connectivity is encapsulated in the Device class
# see Device.py
clientID = carID
# clientID is passed to make possible different clientID
# MQTT doesn't allow different clients with same ID (second is disconnected)
gateway = Device(clientID)


# try connecting in loop
# to handle case in which initially no network connection
while gateway.isConnected() != True:
    try:
        gateway.connect(HOST, PORT, "YES")
    except:
        print('*** Error in MQTT connection !')
        print('\n')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])

    time.sleep(sleepTime)


# to signal MQTT OK blink
led = aiy.voicehat.get_led()

led.set_state(aiy.voicehat.LED.BLINK)

#
# connectivity to OBDII interface
# here it decides if running a simulator or real client
#
if runMode == "ACQUIRE":
    obdii = OBDII()
else:
    # SIMUL
    obdii = OBDIISimulator()

#
# main loop
#

if msgLogging == "YES":
    pFile = open(FNAME, "w")

# wait for MQTT connection OK
# (at this point should be connected)
gateway.wait_for_conn_ok()

# in this point I must insert the SEND for START_TRIP msg
try:
    msgJson = createEventMsg("START_TRIP")

    gateway.publish(TOPIC_ALERTS_NAME, msgJson)
except:
    print('Error in sending START_TRIP...')

nMsgs = 0

while True:
    nMsgs = nMsgs + 1
    print('*** Sending msg n. ', nMsgs)

    # create the msg to send from data
    msgJson = createJSONMsg()

    try:
        time.sleep(0.5)

        led.set_state(aiy.voicehat.LED.ON)

        gateway.publish(TOPIC_NAME, msgJson)

        time.sleep(0.5)

        led.set_state(aiy.voicehat.LED.OFF)
    except:
        print('Error in sending...')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])

    if msgLogging == "YES":
        # log msg on file...
        pFile.write(msgJson)
        pFile.write('\n')

    time.sleep(sleepTime)


if msgLogging == "YES":
    pFile.close()
