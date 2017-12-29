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

class OBDII(object):
    """ This class encapsulate communication with OBD-II interface """

    # Constructor
    def __init__(self):
        self.connOK = False

        print('Connected to OBDII...\n')

    # method definition

    def getMessage(self):
        msg = {}
        msg['value'] = 'test'

        msgJson = json.dumps(msg)

        return msgJson
