#
# Author: L. Saetta
# 27 september 2017
#
# pylint: disable=invalid-name

import json
import time
import sys
from Device import Device

#
# Other Configurations
#
# time between msg send
sleepTime = 5
#the name of MQTT topic where msgs are sent
TOPIC_NAME = 'cardata'

# the name of the file with data
# fName = "raceData_short.log" 

#
# Main
#
print("*******************")
print("Starting simulation....")

#
# reading file name from command line args
#
fName = sys.argv[1]


print("")
print("File name: ", fName)

# MQTT connectivity is encapsulated in Device class
gateway = Device("googx1")

gateway.connect()

nMsgs = 1

# open the input file and then... read, publish loop
try:
    with open(fName) as fp:
        line = fp.readline()

        # wait for MQTT connection OK
        # (at this point should be connected)
        gateway.wait_for_conn_ok()

        # read line by line...    
        while line:
            print(line)

            msgJson = line

            try:
                gateway.publish(TOPIC_NAME, msgJson)
            except:
                print('Error in sending...')

            # sleep before next iteration
            nMsgs += 1
            time.sleep(sleepTime)

            # read next line
            line = fp.readline()
    # end main loop
except IOError:
    print("Errore: file not found: ", fName)
    print("Interrupted...")
    sys.exit(-1)

print()
print("*******************")
print("End of simulation...")
print("Num. of messages processed:", (nMsgs -1))

# close