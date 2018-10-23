# bro
#
# VERSION               0.1

FROM debian:latest as builder
MAINTAINER Anurag Chowdhary <anurag.chowdhary@sjsu.edu>

# Metadata
LABEL program=bro

ENV WD /bro-docker

RUN mkdir ${WD}
WORKDIR /bro-docker

RUN apt-get update && apt-get upgrade -y && echo 2019-09-21 \
  && apt-get -y install build-essential git bison flex gawk cmake swig \
  libmaxminddb-dev python-dev libcurl4-openssl-dev wget libncurses5-dev \
  ca-certificates zlib1g-dev  apt-utils \
  gcc bison cmake flex g++ gdb make libmagic-dev libpcap-dev libgeoip-dev \
  libssl-dev python-dev swig zlib1g-dev git vim python-pip libgoogle-perftools-dev \
  libnuma-dev build-essential python-dev python-pip python-virtualenv \
  libnet1-dev rpcbind openssh-server nmap tcpdump net-tools vim lsb-core \
  lsb-release --no-install-recommends \
  && wget -q http://apt.ntop.org/16.04/all/apt-ntop.deb && dpkg -i apt-ntop.deb \
  && apt-get -y install pfring --no-install-recommends \
  && curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.4.2-amd64.deb && \
  && dpkg -i filebeat-6.4.2-amd64.deb \
  && rm -rf /etc/filebeat/filebeat.yml \
  && git clone --recursive git://git.bro.org/bro \
  && cd bro \
  && git checkout master \
  && ./configure --with-pcap=/opt/pfring \
  && make \
  && make install \
  && export PATH=$PATH:/usr/local/bro/bin \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /bro-docker/*

ADD ./start-service.sh ${WD}/start-service.sh



env PATH /usr/local/bro/bin/:$PATH

RUN ${WD}/start-service.sh
CMD /bin/bash -l
