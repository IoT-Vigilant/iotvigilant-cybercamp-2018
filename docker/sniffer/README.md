# Docker IoTVigilant -- Sniffer
![Docker](https://img.shields.io/badge/docker-running-blue.svg)

## Installation

Modify the **Dockerfile** of this folder and set the *host* and *port* in the environmnet variables were the server will be listening.


To build the docke image run in this directory: `docker build -t iotv_sniffer .`

Run a docker container with iotv_sniffer:
```
sudo su
for dev in $(ifconfig | grep eth | cut -d " " -f 1); do ifconfig $dev promisc; done
docker run -d --net=host iotv_sniffer
```
