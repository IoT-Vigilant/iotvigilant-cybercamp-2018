# Docker IoTVigilant

![Docker](https://img.shields.io/badge/docker-running-blue.svg)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
<p align="center">
<img src="https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018/blob/master/images/logo_docker2.jpg">
</p>

## Installation
- The **Sniffer**: This piece of sotware takes metadata from the packets of the IoT devices and send it the server. You can find how to run it with docker in the [sniffer folder](https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018/tree/master/docker/sniffer)
- The **Server**: Here is were the magic is performed. All the metadata extracted by the sniffer is correlated using a Machine Learning algorithm and the findings are presented in a beautiful web client. You can find how to run it with docker in the [local server folder](https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018/tree/master/docker/local_server)
