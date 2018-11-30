FROM python

RUN apt-get update \ 
    && apt-get upgrade -y \
    && git clone https://github.com/IoT-Vigilant/iotvigilant-cybercamp-2018 /root/iotvigilant \
    && pip3 install -r /root/iotvigilant/docker/sniffer/requirements.txt

WORKDIR /root/iotvigilant

COPY run.sh /root/run.sh

ENTRYPOINT ["/bin/bash", "/root/run.sh"]
