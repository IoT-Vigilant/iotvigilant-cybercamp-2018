# IoTVigilant -- Sniffer (NetFlow)

## Quick Guide

If you want, you can export the metadata of the traffic to the server using netflow (**fprobe**).
To use it you need to install fprobe:

`sudo apt-get install fprobe`

And run it:

`sudo -i <INTERFACE> -fip <SERVER_IP>:<PORT>`

You could filter devices by Mac using the option *-f* with **tcpdump filters**.

If you use this kind of *sniffer* you have to set the host of the **netflow server** and the port were it is going to be listening.
