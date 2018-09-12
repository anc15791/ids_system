#!/bin/bash
#
# This script runs in the tool vm to setup Bro.
# The tool vm is assumed to be Ubuntu 16.04 with management interface eth0.
# The data traffic to be analyzed comes from interface eth1
#

set -e

MAKE_FLAGS="-j$(nproc --all)"
HOME_DIR=$HOME
SRC_DIR="$(dirname $(readlink -f $0))"
echo "* running scripts in directory: $SRC_DIR"
echo " * Update APT"
sudo apt-get update
echo " * Install prerequiste packages"
sudo apt-get -y install default-jdk default-jre gcc bison cmake flex g++ gdb make libmagic-dev libpcap-dev libgeoip-dev libssl-dev python-dev swig zlib1g-dev git vim python-pip libgoogle-perftools-dev libnuma-dev build-essential
echo " * Downloading GeoIP Database"

if [ ! -f "GeoLiteCity.dat" ]; then
  wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz 2> /dev/null
  gzip -d GeoLiteCity.dat.gz
fi

if [ ! -f "GeoLiteCityv6.dat" ]; then
  wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz 2> /dev/null
  gzip -d GeoLiteCityv6.dat.gz
fi

if [ ! -d "/usr/share/GeoIP" ]; then
  sudo mkdir /usr/share/GeoIP
fi
sudo mv GeoLiteCity.dat /usr/share/GeoIP/GeoIPCity.dat
sudo mv GeoLiteCityv6.dat /usr/share/GeoIP/GeoIPCityv6.dat
sleep 2 #settle down time

echo " * Install linux-headers for currently installed version"
sudo apt-get -y install linux-headers-$(uname -r)
sleep 5 #settle down time

echo " * Install pfring 7.2.0 from source"
cd $HOME
wget https://github.com/ntop/PF_RING/archive/7.2.0.tar.gz 2> /dev/null
tar xvzf 7.2.0.tar.gz
cd PF_RING-7.2.0/userland/lib
./configure --prefix=/opt/pfring
sudo make install
sleep 2 #settle down time
cd ../libpcap
./configure --prefix=/opt/pfring
sudo make install
sleep 2 #settle down time
cd ../tcpdump-4.9.2
./configure --prefix=/opt/pfring
sudo make install
sleep 2 #settle down time
cd ../../kernel
sudo make
sudo make install
sleep 2 #settle down time

sudo modprobe pf_ring enable_tx_capture=0 min_num_slots=65534

cd $HOME
echo " * Download BRO repo from github"

if [ ! -d "/users/anurag0/bro" ]; then
  git clone --recursive git://git.bro.org/bro

  echo " * configure and install bro"
  cd bro
  ./configure --with-pcap=/opt/pfring
  sleep 2 #settle down time
  make $MAKE_FLAGS
  sleep 2 #settle down time
  sudo make install
fi

if [ ! -d "/data" ]; then
sudo mkdir /data
fi

if [ ! -d "/data/bro-logs" ]; then
  sudo mkdir /data/bro-logs
fi

if [ ! -d "/data/bro-logs/logs" ]; then
  sudo mv /usr/local/bro/logs /data/bro-logs
fi
sudo ln -sfn /data/bro-logs /usr/local/bro/logs

sudo echo "[[ \":\$PATH:\" != *\":/usr/local/bro/bin:\"* ]] && PATH=\"/usr/local/bro/bin:\${PATH}\"" >> $HOME/.profile
cd $HOME

echo " * Download logstash from https://www.elastic.co/downloads/logstash"
wget https://artifacts.elastic.co/downloads/logstash/logstash-6.3.1.deb 2> /dev/null
sudo dpkg -i logstash-6.3.1.deb
echo " * Copy logstash conf files to /etc/logstash/conf.d/"


sudo cp -a $SRC_DIR/../logstash/.  /etc/logstash/conf.d/

cd $SRC_DIR #$HOME/tools/bro
sudo cp ../logstash.service /etc/systemd/system
sudo cp ../bro.service /etc/systemd/system
echo " * Bro installaton complete"
