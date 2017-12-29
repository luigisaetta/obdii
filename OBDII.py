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

STFORMAT1 = "%Y-%m-%d %H:%M:%S"

class OBDII(object):
    """ This class encapsulate communication with OBD-II interface """

    # Constructor
    def __init__(self):
        self.connOK = False

        print('Connected to OBDII...\n')

    # method definition

    def getMessage(self):
        msg = {}
        msg['dtime'] = datetime.datetime.now().strftime(STFORMAT1)
        msg['ENGINE_LOAD'] = 55.55
        msg['COOLANT_TEMP'] = 33
        msg['RPM'] = 2000
        msg['SPEED'] = 65.1
        msg['RUN_TIME'] = 300
        msg['FUEL_LEVEL'] = 35.5
        msg['AMBIANT_AIR_TEMP'] = 12
        msg['OIL_TEMP'] = 64.3

        return msg
