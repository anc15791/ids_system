# bro
#
# VERSION               0.1

FROM ubuntu:xenial as builder
MAINTAINER Anurag Chowdhary <anurag.chowdhary@sjsu.edu>

# Metadata
LABEL program=bro

ENV WD /bro-docker

RUN mkdir ${WD}
RUN mkdir /data
WORKDIR /bro-docker

RUN apt-get update && apt-get upgrade -y && echo 2019-09-21
RUN apt-get -y install build-essential git bison flex gawk cmake swig libmaxminddb-dev python-dev libcurl4-openssl-dev wget libncurses5-dev ca-certificates zlib1g-dev --no-install-recommends apt-utils
RUN apt-get -y install gcc bison cmake flex g++ gdb make libmagic-dev libpcap-dev libgeoip-dev libssl-dev python-dev swig zlib1g-dev git vim python-pip libgoogle-perftools-dev libnuma-dev build-essential
RUN apt-get -y install python-dev python-pip python-virtualenv
RUN apt-get -y install libnet1-dev rpcbind openssh-server nmap tcpdump net-tools
RUN apt-get -y install vim lsb-core

#Get PF_RING
RUN wget https://github.com/ntop/PF_RING/archive/7.2.0.tar.gz 2> /dev/null
RUN tar xvzf 7.2.0.tar.gz

WORKDIR ${WD}/PF_RING-7.2.0/userland/lib
RUN ./configure --prefix=/opt/pfring
RUN make install

WORKDIR ${WD}/PF_RING-7.2.0/userland/libpcap
RUN ./configure --prefix=/opt/pfring
RUN make install

WORKDIR ${WD}/PF_RING-7.2.0/userland/tcpdump-4.9.2
RUN ./configure --prefix=/opt/pfring
RUN make install


WORKDIR ${WD}
RUN apt-get update && \
    apt-get -y -q install wget lsb-release && \
    wget -q http://apt.ntop.org/16.04/all/apt-ntop.deb && dpkg -i apt-ntop.deb && \
    apt-get clean all && \
    apt-get update && \
    apt-get -y install pfring


curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.4.2-amd64.deb
dpkg -i filebeat-6.4.2-amd64.deb
RUN rm -rf /etc/filebeat/filebeat.yml
ADD ./common/filebeat.yml /etc/filebeat/filebeat.yml

#Checkout bro
# Build bro
RUN git clone --recursive git://git.bro.org/bro
ADD ./common/gitbro ${WD}/common/gitbro
RUN ${WD}/common/gitbro master
RUN ln -s /usr/local/bro/logs /data/bro-logs

# get geoip data

RUN apt-get update && apt-get -y install wget ca-certificates --no-install-recommends
ADD ./common/getmmdb.sh /usr/local/bin/getmmdb.sh
RUN /usr/local/bin/getmmdb.sh


ADD ./common/bro_profile.sh /etc/profile.d/bro.sh
ADD ./start-service.sh ${WD}/start-service.sh

env PATH /usr/local/bro/bin/:$PATH

RUN ${WD}/start-service.sh
CMD /bin/bash -l
