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

ADD ./start-service.sh ${WD}/start-service.sh

RUN apt-get update && apt-get upgrade -y && echo 2019-09-21 \
  && apt-get -y install build-essential git gawk cmake swig \
  libmaxminddb-dev python-dev libcurl4-openssl-dev wget libncurses5-dev \
  ca-certificates zlib1g-dev  apt-utils \
  gcc bison cmake flex g++ gdb make libmagic-dev libpcap-dev libgeoip-dev \
  libssl-dev git vim python-pip libgoogle-perftools-dev \
  libnuma-dev  python-virtualenv \
  libnet1-dev rpcbind openssh-server nmap tcpdump net-tools lsb-core \
  lsb-release curl gnupg2\
  && apt-get update \
  && wget http://apt-stable.ntop.org/stretch/all/apt-ntop-stable.deb \
  && dpkg -i apt-ntop-stable.deb \
  && apt-get clean all \
  && apt-get update \
  && apt-get -y install pfring nprobe ntopng ntopng-data n2disk cento pfring-drivers-zc-dkms \
  && curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.4.2-amd64.deb \
  && dpkg -i filebeat-6.4.2-amd64.deb \
  && rm -rf /etc/filebeat/filebeat.yml \
  && apt-get update \
  && git clone --recursive git://git.bro.org/bro \
  && cd bro \
  && git checkout master \
  && LDFLAGS="-lpfring -lpcap" ./configure --with-pcap=/usr/local/lib \
  && make -j4 \
  && make install \
  # && ldd /usr/local/bro/bin/bro | grep pcap libpcap.so.1 => /usr/local/lib/libpcap.so.1 \
  && export PATH=$PATH:/usr/local/bro/bin \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /bro-docker/* \
  && rm -rf /usr/local/bro/etc/broctl.cfg \
  && rm -rf /usr/local/bro/etc/node.cfg \
  && rm -rf /usr/local/bro/etc/networks.cfg \
  && rm -rf /usr/local/bro/share/bro/site/local.bro \
  && export PATH=$PATH:/usr/local/bro/bin \
  && echo "redef LogAscii::use_json = T;" >> /usr/local/bro/share/bro/base/frameworks/logging/writers/ascii.bro \
  && rm -rf /etc/filebeat.yml

env PATH /usr/local/bro/bin/:$PATH

RUN ${WD}/start-service.sh
CMD /bin/bash -l



# && wget -nv http://download.opensuse.org/repositories/network:bro/Debian_8.0/Release.key -O Release.key \
# && apt-key add - < Release.key \
# && apt-get update \
# && echo 'deb http://download.opensuse.org/repositories/network:/bro/Debian_8.0/ /' >> /etc/apt/sources.list.d/bro.list  \
# && apt-get update \
# && apt-get dist-upgrade \
# && apt-get install -f bro-core libbroccoli broctl  bro \
