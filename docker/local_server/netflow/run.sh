#!/bin/bash
nfcapd -p 2055 -b 0.0.0.0 -l /tmp/netflowpckts -D -x "python3 /root/iotvigilant/local_server/netflow/parse_netflow.py /tmp/netflowpckts"
