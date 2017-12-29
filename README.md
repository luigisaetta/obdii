# OBDII
#
## Author: L. Saetta

## Starting Date:   27/12/2017
## Last update:     29/12/2017
##                  luigi.saetta@gmail.com

This repository contains most of the work I have done to develop, in Python,
a working prototype for my idea of a connected car.

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

Release 1.0:
This release is to test the OBDII interface and demonstrate that the project is feasible.
The first release of the code will read, in a loop, a set of values from OBDII interface, format it as a JSON msg
and will send it to the MQTT broker to a dedicated topic.
Communication will be secure and protected using TLS1.2.
QoS for msgs will be: 1 (guaranteed at least once).
In a separate project I will create a NodeRED flow to show the data from the car in a Dashboard.

Release 2.0:
In release 2.0 I will integrate Oracle IoT Cloud Service and Oracle IoT Fleet Management.

Release 3.0:
I will integrate the Python code with Eclipse Kura.


Release history:
- 27/12/2017: vers. 0.5

