# OBDII
#
## Author: L. Saetta

## Starting Date:   27/12/2017
## Last update:     01/01/2018
##                  luigi.saetta@gmail.com

This repository contains most of the work I have done to develop, in Python,
a working prototype for my idea of a Connected Car.

Following, some details:

HW that will be used:

- OBDII port in the car
- OBDII bluetooth adapter (available from Amazon, for example)
- a Raspberry PI 3 (need bluetooth and WIFI)
- A SmartPhone, for Internet Connectivity (in my case an iPhone)
- a PowerBank, to power the RPI

Cloud Services:

- MQTT broker (TLS capable)
- NodeRED, to process msgs

Dependencies:
- Paho MQTT client for Python (see: https://www.eclipse.org/paho/clients/python/)
- configparser
- Python-OBD (see credits)

Release 0.6:
This release is to test the OBDII interface and demonstrate that the project is feasible.
The first release of the code will read, in a loop, a set of values from OBDII interface, format it as a JSON msg
and will send it to the MQTT broker to a dedicated topic.
Communication will be secure and protected using TLS1.2.
QoS for msgs will be: 1 (guaranteed at least once).
In a separate project I will create a NodeRED flow to show the data from the car in a Dashboard.

Release 0.7:
OBD2 becomes a system service on RPI, therefore is automatically stared on RPI startup!

Release 1.0:
Production ready code with all the features described for vers. 0.6

Release 2.0:
In release 2.0 I will integrate Oracle IoT Cloud Service and Oracle IoT Fleet Management.

Release 3.0:
I will integrate the Python code with Eclipse Kura.


Release history:
- 29/12/2017: vers. 0.6
- 01/01/2018: vers. 0.7


For more information about OBD-II, see https://en.wikipedia.org/wiki/OBD-II_PIDs

Credits:
- Access in Python code to OBDII data is realized using Python-OBD, see http://python-obd.readthedocs.io/en/latest/

