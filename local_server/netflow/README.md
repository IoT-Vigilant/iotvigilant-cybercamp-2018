# IoTVigilant -- Sniffer (NetFlow)

## Quick Guide

In order to capture the metadata sent by the *neflox nodes* it is needed to install **nfdump**:

`sudo apt-get install nfdump`

Then, you have to start **nfcapd** (it will be listening in a port to capture the metadata provided by the nodes):

```
mkdir /tmp/netflowpckts
nfcapd -p <PORT> -b 0.0.0.0 -l /tmp/netflowpckts -D -x "python3 /opt/iotvigilant/local_server/parse_netflow.py /tmp/netflowpckts"
```

Parameters:
- -p: Port were the metadata has to go
- -b: Listen in 0.0.0.0
- -l: Path were the logs will be saved
- -D: Run in background
- -x: Execute the script each time a new log file is created
