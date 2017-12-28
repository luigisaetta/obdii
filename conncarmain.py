#
# Author:       L. Saetta
# created:      27 december 2017
# last update:  27/12/2017
#
# published under MIT license (see LICENSE file)

# pylint: disable=invalid-name

import json
import time
import datetime
import configparser
from Device import Device

# Configuration
#  to format datetime
STFORMAT1 = "%Y-%m-%d %H:%M:%S"
STFORMAT2 = "%Y-%m-%d"

# file name for local logging
FNAME = "msgs" + datetime.datetime.now().strftime(STFORMAT2) + ".log"

# send a msg every 5 sec.
sleepTime = 5
#the name of MQTT topic where msgs are sent
TOPIC_NAME = 'cardata'


# read configuration from gateway.ini file
config = configparser.ConfigParser()
config.read('gateway.ini')
msgLogging = config['DEFAULT']['msgLogging']
carID = config['DEFAULT']['carID']

#
# createJSONMsg()
# create the msg in JSON format starting from OBDII readings
#
def createJSONMsg():
    # for now simulate
    msg['carid'] = carID
    msg['dtime'] = datetime.datetime.now().strftime(STFORMAT1)
    msg['rpm'] = 1200
    msg['speed'] = 35
    msg['relposacc'] = 10
    msg['tcoolant'] = 33
    msg['toutdoor'] = 12
    
    msgJson = json.dumps(msg)
    
    return msgJson


#
# **** Main **** 
#

# MQTT connectivity is encapsulated in the Device class
# see Device.py
gateway = Device()


# try connecting in loop
# to handle case in which initially no network connection
while gateway.isConnected() != True:
    try:
        gateway.connect()
    except:
        print('Error in MQTT connection !')

    time.sleep(sleepTime)


#
# main loop
#

if msgLogging == "YES":
    pFile = open(FNAME, "w")

# wait for MQTT connection OK
# (at this point should be connected)
gateway.wait_for_conn_ok()

print('Mqtt connection OK !')

nMsgs = 0
msg = {}

while True:
    nMsgs = nMsgs + 1
    print('Sending msg number: ', nMsgs)

    # create the msg to send from data
    msgJson = createJSONMsg()

    try:
        gateway.publish(TOPIC_NAME, msgJson)
    except:
        print('Error in sending...')

    if msgLogging == "YES":
        # log msg on file...
        pFile.write(msgJson)
        pFile.write('\n')

    time.sleep(sleepTime)


if msgLogging == "YES":
    pFile.close()
