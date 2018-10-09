# logstash
#
# VERSION               0.1

FROM ubuntu:xenial as base
MAINTAINER Anurag Chowdhary <anurag.chowdhary@sjsu.edu>

# Metadata
LABEL program=logstash

ENV WD /logstash

RUN mkdir ${WD}

WORKDIR ${WD}

RUN apt-get update && apt-get upgrade -y && echo 2019-09-21
RUN apt-get -y install build-essential git gawk cmake swig libmaxminddb-dev libcurl4-openssl-dev wget libncurses5-dev ca-certificates zlib1g-dev default-jdk default-jre --no-install-recommends apt-utils
RUN apt-get -y install gcc bison cmake flex g++ gdb make libmagic-dev libpcap-dev libgeoip-dev libssl-dev swig zlib1g-dev vim libgoogle-perftools-dev libnuma-dev build-essential
RUN apt-get -y install python-dev python-pip python-virtualenv
RUN apt-get -y install libnet1-dev rpcbind openssh-server nmap tcpreplay tcpdump net-tools curl
RUN apt-get -y install vim lsb-core


RUN wget https://artifacts.elastic.co/downloads/logstash/logstash-6.4.0.deb 2> /dev/null
RUN dpkg -i logstash-6.4.0.deb

COPY configs/. /etc/logstash/conf.d/
COPY ./logstash.service /etc/systemd/system/

CMD /usr/share/logstash/bin/logstash --path.settings /etc/logstash -f /etc/logstash/conf.d --config.reload.automatic
