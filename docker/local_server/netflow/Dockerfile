FROM python

RUN apt-get update \ 
    && apt-get upgrade -y \
    && apt-get install nfdump -y \
    && git clone https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018 /root/iotvigilant \
    && pip3 install elasticsearch \
    && mkdir /tmp/netflowpckts

WORKDIR /root/iotvigilant

COPY run.sh /root/run.sh

#ENTRYPOINT ["/bin/bash", "/root/run.sh"]
