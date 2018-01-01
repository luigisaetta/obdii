"""
#
# Author:       L. Saetta
# created:      01 january 2018
# last update:  01/01/2018
#
# published under MIT license (see LICENSE file)
#
# This module implement a command processor
#
# Class providing methods to interact with MQTT broker
# L.S. 2017
#
"""

# pylint: disable=invalid-name

import json
import time
import datetime
import sys
import configparser
import os
from Device import Device

# Configuration
#  to format datetime
STFORMAT1 = "%d-%m-%Y %H:%M:%S"
STFORMAT2 = "%d-%m-%Y"

# read configuration from gateway.ini file
# read OBD2_HOME env variable
OBD2HOME = os.getenv('OBD2_HOME')

config = configparser.ConfigParser()
config.read(OBD2HOME + '/gateway.ini')
msgLogging = config['DEFAULT']['msgLogging']
carID = config['DEFAULT']['carID']

TOPIC_COMMAND = 'carcommands/' + carID

print('Reading commands from topic: ', TOPIC_COMMAND)

# time between connections attempt
sleepTime = 2

#
# **** Main **** 
#

# MQTT connectivity is encapsulated in the Device class
# see Device.py
clientID = carID + "SUB"

gateway = Device(clientID)

# try connecting in loop
# to handle case in which initially no network connection
while gateway.isConnected() != True:
    try:
        gateway.connect()
    except:
        print('Error in MQTT connection !')

    time.sleep(sleepTime)

# wait for MQTT connection OK
# (at this point should be connected)
gateway.wait_for_conn_ok()

# Subscribes to the topic dedicated to the Car
gateway.subscribe(TOPIC_COMMAND)

while True:
    # waiting for commands
    time.sleep(sleepTime)
