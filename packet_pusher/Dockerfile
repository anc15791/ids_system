# packet pusher
#
# VERSION               0.1

FROM ubuntu:xenial as builder
MAINTAINER Anurag Chowdhary <anurag.chowdhary@sjsu.edu>

# Metadata
LABEL program=packerpusher

ENV WD /packet_pusher

RUN mkdir ${WD}

WORKDIR ${WD}

RUN apt-get update && apt-get upgrade -y && echo 2019-09-21
RUN apt-get -y install build-essential git gawk cmake swig libmaxminddb-dev libcurl4-openssl-dev wget libncurses5-dev ca-certificates zlib1g-dev --no-install-recommends apt-utils
RUN apt-get -y install gcc bison cmake flex g++ gdb make libmagic-dev libpcap-dev libgeoip-dev libssl-dev swig zlib1g-dev vim libgoogle-perftools-dev libnuma-dev build-essential
RUN apt-get -y install python-dev python-pip python-virtualenv
RUN apt-get -y install libnet1-dev rpcbind openssh-server nmap tcpreplay tcpdump net-tools
RUN apt-get -y install vim lsb-core

COPY pcaps ${WD}/pcaps
COPY schema ${WD}/schema
COPY src ${WD}/src

CMD /bin/bash -l
