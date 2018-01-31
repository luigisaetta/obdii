import configparser
import os
import serial
import time
import json
from Device import Device

#
# globals
#
#the name of MQTT topic where msgs are sent
TOPIC_GPS = 'owntracks/luigi/googx1'
sleepTime = 5

#
# functions definition
#

# transforms lat e lon in decimal
def calcola_dec(x):
    DD = int(float(x)/100)
    SS = float(x) - DD * 100
    Dec = DD + SS/60
    return Dec

def get_lat(gps):
    lat = gps[18:22].decode("utf-8")  + "." + gps[23:27].decode("utf-8") 
    # transform in decimal
    return calcola_dec(lat)

def get_lon(gps):
    lon = gps[30:35].decode("utf-8")  + "." + gps[36:40].decode("utf-8")
    # transform in decimal
    return calcola_dec(lon)

def get_alt(gps):
    # for now, it's a fake
    alt = 10
    return alt

#
# Main
#
# read configuration from gateway.ini file
# read OBD2_HOME env variable
OBD2HOME = os.getenv('OBD2_HOME')

config = configparser.ConfigParser()
config.read(OBD2HOME + '/gateway.ini')
msgLogging = config['DEFAULT']['msgLogging']
carID = config['DEFAULT']['carID']

# clientID is passed to make possible different clientID
# MQTT doesn't allow different clients with same ID (second is disconnected)
gateway = Device("gx1gps")

# init serial
ser = serial.Serial('/dev/ttyUSB0', 4800, timeout = None)

# try connecting in loop
# to handle case in which initially no network connection
while gateway.isConnected() != True:
    try:
        gateway.connect("localhost", 1883)
    except:
        print('*** Error in MQTT connection !')

    time.sleep(sleepTime)

#
# main loop
#
while True:
   gps = ser.readline()
   
   # print all NMEA strings with a GPS fix, only if there is a fix (1)
   if gps[1 : 6] == b'GPGGA':
       # check if there is a fix
       if gps[43:44] == b'1':
           lat = get_lat(gps)
           lon = get_lon(gps)
           alt = get_alt(gps)

           print(lat, lon, alt)

           # build JSON msg and send to topic on localhost

