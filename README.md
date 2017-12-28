# obdii
#
## Author: L. Saetta

## Date:   27/12/2017
##         luigi.saetta@gmail.com

This repository contains most of the work I have done to develop, in Python,
a working prototype for my idea of a connected car.

Some details:

HW that will be used

- OBDII port in car
- OBDII bluetooth adapter (from Amazon)
- RPI 3
- A SmartPhone (in my case an iPhone)
- a PowerBank

Cloud Services:

- an MQTT broker
- NodeRED, to process msgs

Release 1.0
The first release of the code will read a set of values from OBDII interface, will format it as a JSON msg
and will send it to the MQTT broker to a dedicated topic.
In a separate project I will create a flow using NodeRED to show the data from the car in a Dashboard.

Release 2.0
In release 2.0 I will integrate Oracle IoT Cloud Service

Release history;
27/12/2017: vers. 0.5

