"""
#
# Author:       L. Saetta
# created:      29 december 2017
# last update:  29/12/2017
#
# published under MIT license (see LICENSE file)
"""

# pylint: disable=invalid-name

import json
import datetime
import obd 
import configparser


# config
config = configparser.ConfigParser()
config.read('gateway.ini')

OBDDATA_FORMAT_STRING = config['DEFAULT']['OBDDATA_FORMAT_STRING']
STFORMAT1 = "%d-%m-%Y %H:%M:%S"

class OBDII(object):
    """ This class encapsulate communication with OBD-II interface """

    # Constructor
    def __init__(self):
        self.connOK = False
        
        # create the connection
        self.obdconn = obd.OBD()

        print('OBD connection status: ', self.obdconn.status())

        # TODO: here I can add a check to see if it is connected
        # and eventually retry the connection...
        #
        self.connOK = True

        print('Connected to OBDII...\n')

    # method definition

    # utility method to format float with a fixed number of decimals
    def format_float(self, value):
        return float(OBDDATA_FORMAT_STRING.format(value))
    
    # methods reading value from OBDII interface
    def getENGINELOAD(self):
        cmd = obd.commands.ENGINE_LOAD

        return self.format_float(self.getValue(cmd))
    
    def getCOOLANTTEMP(self):
        cmd = obd.commands.COOLANT_TEMP

        return self.getValue(cmd)

    def getRPM(self):
        cmd = obd.commands.RPM

        return self.getValue(cmd)

    def getSPEED(self):
        cmd = obd.commands.SPEED

        return self.getValue(cmd)
    
    def getRUNTIME(self):
        cmd = obd.commands.RUN_TIME

        return self.getValue(cmd)
    
    def getFUELLEVEL(self):
        cmd = obd.commands.FUEL_LEVEL

        return self.getValue(cmd)

    def getAMBIANTAIRTEMP(self):
        cmd = obd.commands.AMBIANT_AIR_TEMP

        return self.getValue(cmd)
    
    def getOILTEMP(self):
        cmd = obd.commands.OIL_TEMP

        return self.getValue(cmd)

    def getValue(self, cmd):
        response = self.obdconn.query(cmd)

        return response.value.magnitude

    def getMessage(self):
        msg = {}
        msg['DTIME'] = datetime.datetime.now().strftime(STFORMAT1)
        msg['ENGINE_LOAD'] = self.getENGINELOAD()
        msg['COOLANT_TEMP'] = self.getCOOLANTTEMP()
        msg['RPM'] = self.getRPM()
        msg['SPEED'] = self.getSPEED()
        msg['RUN_TIME'] = self.getRUNTIME()
        # msg['FUEL_LEVEL'] = self.getFUELLEVEL()
        msg['AMBIANT_AIR_TEMP'] = self.getAMBIANTAIRTEMP()
        # msg['OIL_TEMP'] = self.getOILTEMP()

        return msg
