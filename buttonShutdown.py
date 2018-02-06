import configparser
import datetime
import json
import os
import sys
import time
from subprocess import call
from Device import Device

# only if using Googe Voice
sys.path.append('/home/pi/AIY-voice-kit-python/src')
import aiy.voicehat

# globals
TOPIC_ALERTS_NAME = "caralerts"
sleepTime = 5
# used for STOP_TRIP msg
STFORMAT3 = "%d-%m-%Y %H"

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


def on_button_press():
    button.on_press(None)
    print('The button is pressed!')
    time.sleep(3)
    print('Shutting down...')

    # here I should add the code to send STOP_TRIP alert

    # in this point I must insert the SEND for START_TRIP msg
    try:
        msgJson = createEventMsg("STOP_TRIP")

        gateway.publish(TOPIC_ALERTS_NAME, msgJson)
    except:
        print('Error in sending STOP_TRIP...')

    call("sudo shutdown -h now", shell=True)


#
# main
#
# read configuration from gateway.ini file
# read OBD2_HOME env variable
OBD2HOME = os.getenv('OBD2_HOME')

config = configparser.ConfigParser()
config.read(OBD2HOME + '/gateway.ini')

carID = config['DEFAULT']['carID']

# should be read from config file
HOST = "ubuntucontainers-dashboariotnew-zekci6cs.srv.ravcloud.com"
PORT = 8883

# clientID is passed to make possible different clientID
# MQTT doesn't allow different clients with same ID (second is disconnected)
gateway = Device("googshut1")

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

button = aiy.voicehat.get_button()
button.on_press(on_button_press)

while True:
    print('Another loop...')
    time.sleep(5)
