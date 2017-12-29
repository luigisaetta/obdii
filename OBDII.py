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
    def getValueENGINELOAD(self):
        cmd = obd.commands.ENGINE_LOAD

        return self.getValue(cmd)
    
    def getValueCOOLANTTEMP(self):
        cmd = obd.commands.COOLANT_TEMP

        return self.getValue(cmd)

    def getValueRPM(self):
        cmd = obd.commands.RPM

        return self.getValue(cmd)

    def getValueSPEED(self):
        cmd = obd.commands.SPEED

        return self.getValue(cmd)
    
    def getValueRUNTIME(self):
        cmd = obd.commands.RUN_TIME

        return self.getValue(cmd)
    
    def getValueFUELLEVEL(self):
        cmd = obd.commands.FUEL_LEVEL

        return self.getValue(cmd)

    def getValueAMBIANTAIRTEMP(self):
        cmd = obd.commands.AMBIANT_AIR_TEMP

        return self.getValue(cmd)
    
    def getValueOILTEMP(self):
        cmd = obd.commands.OIL_TEMP

        return self.getValue(cmd)

    def getValue(self, cmd):
        response = self.obdconn.query(cmd)

        return response.value.magnitude

    def getMessage(self):
        msg = {}
        msg['DTIME'] = datetime.datetime.now().strftime(STFORMAT1)
        msg['ENGINE_LOAD'] = self.getValueENGINELOAD()
        msg['COOLANT_TEMP'] = self.getValueCOOLANTTEMP()
        msg['RPM'] = self.getValueRPM()
        msg['SPEED'] = self.getValueSPEED()
        msg['RUN_TIME'] = self.getValueRUNTIME()
        msg['FUEL_LEVEL'] = self.getValueFUELLEVEL()
        msg['AMBIANT_AIR_TEMP'] = self.getValueAMBIANTAIRTEMP()
        msg['OIL_TEMP'] = self.getValueOILTEMP()

        return msg
