"""
#
# Author:       L. Saetta
# created:      01 january 2018
# last update:  01/01/2018
#
# published under MIT license (see LICENSE file)
#
# This module implement a command processor
# published under MIT license (see LICENSE file)
#
"""

# pylint: disable=invalid-name

import configparser
import datetime
import json
import os
import sys
import time

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
fNameCommands = OBD2HOME + "/" + config['DEFAULT']['COMMAND_LOG']

TOPIC_COMMAND = 'carcommands/' + carID

# time between connections attempt
sleepTime = 2


def receive_msgs(mqttc, obj, msg):
    # example of valid msg for TEST
    # {"CARID":"0001", "DTIME":"01-01-2018 18:15:26","COMM_TYPE":"PRINT","PARAMS":[]}
    
    validMsg = {"CARID":"0001", "SENDER":"TEST",
               "DTIME":"01-01-2018 18:15:26","COMM_TYPE":"PRINT","PARAMS":[1,"pippo"]}

    print('\n')
    print('Received command to process: ')

    try:
        # first need to check carID
        msgJson = json.loads(msg.payload.decode("utf-8"))

        if msgJson['CARID'] == carID:
            # OK to process msg
            process_msgs(msg)
        else:
            # ignore msg, do nothing
            pass
    except:
        print('\n')
        print('*** Error in parsing command: ')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])
        print('*** Command received: ', msg.payload)


def process_msgs(msg):
    # here we define the only commands supported
    # insert here other commands...
    options = {"PRINT": doPrint,
               "BLINK": doBlink,
               "OTHERS": doOthers
               }

    try:
        msgJson = json.loads(msg.payload.decode("utf-8"))

        print('CARID: ', msgJson['CARID'])
        print('DTIME: ', msgJson['DTIME'])
        print('SENDER: ', msgJson['SENDER'])
        print('COMMAND: ', msgJson['COMM_TYPE'])
        print('PARAMS: ', msgJson['PARAMS'])

        # logging
        pFileCommands.write(str(msg.payload) + "\n")
        pFileCommands.flush()

        # here we call the function handling the single command
        # it serches the name of the func in the dictionary options !!!
        options[msgJson['COMM_TYPE']](msgJson['COMM_TYPE'], msgJson['PARAMS'])
    except:
        print('\n')
        print('*** Error in parsing command: ')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])
        print('*** Command received: ', msg.payload)

#
# These are the functions dedicated to single commands
# TODO: put the code to implement commands
#
def doPrint(commType, parms):
    print('*** Executing Print command ...')


def doBlink(commType, parms):
    print('*** Executing Blink command ...')


def doOthers(commType, parms):
    print('*** Executing Others command ...')


#
# **** Main ****
#

print("")
print("***")
print("*** OBD2 Command Processor started ***")
print("***")

print('*** Reading commands from topic: ', TOPIC_COMMAND)

# MQTT connectivity is encapsulated in the Device class
# see Device.py
# assign a different clientID (+SUB)
clientID = carID + "SUB"

gateway = Device(clientID)

# try connecting in loop
# to handle case in which initially no network connection
while gateway.isConnected() != True:
    try:
        gateway.connect()
    except:
        print('*** Error in MQTT connection !')

    time.sleep(sleepTime)

# wait for MQTT connection OK
# (at this point should be connected)
gateway.wait_for_conn_ok()

# Subscribes to the topic dedicated to the Car
gateway.subscribe(TOPIC_COMMAND)

# redefine here the fcallback to call when msg received
gateway.set_on_message(receive_msgs)

# file for logging commands
pFileCommands = open(fNameCommands, "w")

while True:
    # waiting for commands
    time.sleep(sleepTime)
