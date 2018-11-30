# Docker IoTVigilant -- Sniffer
![Docker](https://img.shields.io/badge/docker-running-blue.svg)

## Installation

Modify the **Dockerfile** of this folder and set the *host* and *port* in the environmnet variables were the server will be listening.


To **build** the docker image run in this directory: `docker build -t iotv_sniffer .`

**Run** a docker container with **iotv_sniffer**:
```
sudo su
for dev in $(ifconfig | grep eth | cut -d " " -f 1); do ifconfig $dev promisc; done
docker run -d [--env IOTV_SERVER "192.168.40.100" --env IOTV_PORT "5001" --env IOTV_TIME "300000"] --net=host iotv_sniffer
```

**Default** values are:
- IOTV_SERVER = 127.0.0.1
- IOTV_PORT = 5001
- IOTV_TIME = 300000 (ms)
