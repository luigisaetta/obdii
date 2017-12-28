#
# Author: L. Saetta
# 27 december 2017
#
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

FNAME = "msgs" + datetime.datetime.now().strftime(STFORMAT2) + ".txt"

# send a msg every 10 sec.
sleepTime = 10
#MQTT topic
TOPIC_NAME = 'cardata'


# read config from ini file
config = configparser.ConfigParser()
config.read('gateway.ini')
msgLogging = config['DEFAULT']['msgLogging']

def setFields():
    # for now simulate
    msg['carid'] = '0001'
    msg['dtime'] = datetime.datetime.now().strftime(STFORMAT1)
    msg['rpm'] = 1200
    msg['speed'] = 35
    msg['relposacc'] = 10
    msg['tcoolant'] = 33
    msg['toutdoor'] = 12
    
    msgJson = json.dumps(msg)
    
    return msgJson

#
# Main 
#

# MQTT connectivity is encapsulated in the Device class
# see Device.py
gateway = Device()

gateway.connect()

nMsgs = 0

#
# main loop
#

if msgLogging == "YES":
    pFile = open(FNAME, "w")

# wait for MQTT connection OK
# (at this point should be connected)
gateway.wait_for_conn_ok()

print('Mqtt connected OK!')

msg = {}

while True:
    nMsgs = nMsgs + 1
    print('Sending msg ', nMsgs)

    # create the msg to send from data
    msgJson = setFields()

    gateway.publish(TOPIC_NAME, msgJson)
    
    if msgLogging == "YES":
        # log msg on file...
        pFile.write(msgJson)
        pFile.write('\n')

    time.sleep(sleepTime)


if msgLogging == "YES":
    pFile.close()
