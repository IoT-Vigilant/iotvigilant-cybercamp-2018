# Iotvigilant-Cybercamp-2018
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)



IoTVigilant is an Open Source development created to detect :shipit: weird network behaviors of IoT devices --or of any device with low network interaction--.

## Basic Overview

Nowadays, more and more IoT devices are being used and, as these devices aren't created with security in mind, they represent a huge security risk in the cyber world. For example, in 2016 Miraia :imp: was an IoT botnet which size varied from 800,000 infected devices to 2.5 million and was used to perform DDoS attacks to some Internet services.

In spite of the size of this botnet, it isn't the biggest IoT botnet that has been used to perform attacks around the Internet :disappointed_relieved:. This is why we think that this proyect is needed to discover when a IoT device is behaving in a weird way to stop it :innocent:.

### Protect from the network

As the user of an IoT device rarely has access to the source code of his device and won't be able to install any security meassure inside it :see_no_evil:, the best way to discover that the gadget has been infected :alien: and is performing unexpected actions, is monitoring the network where it's connected.

## IoTVigilant

This proyect is composed of 2 parts:
- **The Sniffer**: This piece of sotware takes metadata from the packets of the IoT devices and send it the server. You can find more information about this in the [Sniffer folder](https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018/tree/master/sniffer).
- **The Server**: Here is were the magic is performed. All the metadata extracted by the sniffer is correlated using a Machine Learning algorithm and the findings are presented in a beautiful web client. You can find more information about how the server works in the [Local Server folder](https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018/tree/master/local_server).


If you are a **Docker** fan, the you can find an installation guide of the **Sniffer** and the **Server** in the [Docker folder](https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018/tree/master/docker).

## Machine Learning Algorithm


