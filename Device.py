"""
#
# Author:       L. Saetta
# created:      10 december 2017
# last update:  29/12/2017
#
# published under MIT license (see LICENSE file)
#
# This module implement a class representing a Device
#
# Class providing methods to interact with MQTT broker
# L.S. 2017
#
"""
# pylint: disable=invalid-name

import time
import configparser
import os
import paho.mqtt.client as mqtt


#
# Configuration for MQTT protocol
# is written in gateway.ini file !
# host is the broker, in my Ravello env
# read OBD2_HOME env variable
OBD2HOME = os.getenv('OBD2_HOME')
config = configparser.ConfigParser()
config.read(OBD2HOME + '/gateway.ini')

HOST = config['DEFAULT']['host']
PORT = int(config['DEFAULT']['port'])
TIMEOUT = int(config['DEFAULT']['timeout'])
CLIENT = config['DEFAULT']['client']
MYQOS = int(config['DEFAULT']['myQos'])
mqttLogging = config['DEFAULT']['mqttLogging']
# config to enable TLS
TLS = config['DEFAULT']['TLS']
CAFILEPATH = config['DEFAULT']['CAFILEPATH']

class Device(object):
    """ This class encapsulate Device communication with MQTT broker """

    # Constructor
    def __init__(self):
        self.connOK = False

        # Create MQTT client and set MQTT client ID
        self.mqttClient = mqtt.Client(CLIENT, protocol=mqtt.MQTTv311)
        # note that the client id must be unique on the broker

        # MQTT callbacks registration
        self.mqttClient.on_message = self.on_message
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_disconnect = self.on_disconnect

        self.mqttClient.on_publish = self.on_publish

        if mqttLogging == "YES":
            self.mqttClient.on_log = self.on_log

    # MQTT callbacks definition

    def on_connect(self, mqttc, obj, flags, connResult):

        if connResult == 0:
            self.connOK = True

        print("")
        print("MQTT Connection:...: ", self.connOK)
        print("")

    def on_disconnect(self, client, userdata, rc):
        self.connOK = False
        print("MQTT disconnected...")

    def isConnected(self):
        return self.connOK

    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        # print("mid: " + str(mid))
        pass

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    # end MQTT callbacks definition

    #
    # Public Methods
    #
    def connect(self):
        if TLS == "YES":
            # this is the path to CA crt file (needed)
            self.mqttClient.tls_set(ca_certs=CAFILEPATH)
        
        self.mqttClient.connect(HOST, PORT, TIMEOUT)

        # start a background thread to process networks events. It should also
        # handle automatical reconnection...
        self.mqttClient.loop_start()

    def wait_for_conn_ok(self):
        while self.connOK != True:
            print("Waiting for MQTT connection...")
            time.sleep(1)

    def publish(self, topic, msg):
        if mqttLogging == "YES":
            print("message published ", msg)

        (result, mid) = self.mqttClient.publish(topic, msg, qos=MYQOS)

    def subscribe(self, topic):
        # for now not implemented
        pass
