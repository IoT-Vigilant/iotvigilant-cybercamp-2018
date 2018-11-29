# Docker IoTVigilant -- Sniffer
![Docker](https://img.shields.io/badge/docker-running-blue.svg)

## Installation

Modify the **Dockerfile** of this folder and set the *host* and *port* in the environmnet variables were the server will be listening.


Then run: `docker build -t iotv_sniffer .`

`
sudo su
for dev in $(ifconfig | grep eth | cut -d " " -f 1); do ifconfig $dev promisc; done
docker run -d --net=host iotv_sniffer
`
