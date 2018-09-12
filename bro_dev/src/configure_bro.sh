#!/bin/bash
#
# Scripts to configure  BRO

if [ $# -ne 5 ]
  then
    echo "$0 <interface> <lb_processes> <pin_cpu_list> <analytics_ip> <analytics_port>"
    exit 1
fi
INTERFACE=$1
LB_PROCESSES=$2
CPU_LIST=$3
LB_METHOD="pf_ring"
ANA_IP=$4
ANA_PORT=$5

echo " * set node.cfg in bro"
sudo cp $HOME/ids_system/scripts/node.cfg  /usr/local/bro/etc/node.cfg
sudo cp $HOME/ids_system/scripts/broctl.cfg /usr/local/bro/etc/broctl.cfg

sudo echo "redef LogAscii::use_json = T;" >> /usr/local/bro/share/bro/base/frameworks/logging/writers/ascii.bro
sudo echo "redef ignore_checksums = T;" >> /usr/local/bro/share/bro/site/local.bro
sleep 2 #settle down time

sudo sed -i "s/_INTERFACE_/$INTERFACE/" /usr/local/bro/etc/node.cfg
sudo sed -i "s/_LOAD_BALANCE_PROCESSES_/$LB_PROCESSES/" /usr/local/bro/etc/node.cfg
sudo sed -i "s/_CPU_LIST_/$CPU_LIST/" /usr/local/bro/etc/node.cfg
sudo sed -i "s/_LB_METHOD_/$LB_METHOD/" /usr/local/bro/etc/node.cfg
echo " * BRO configuration complete"

sudo sed -i "s/_ANA_IP_/$ANA_IP/" /etc/logstash/conf.d/logstash.conf
sudo sed -i "s/_ANA_PORT_/$ANA_PORT/" /etc/logstash/conf.d/logstash.conf
echo " * Logstash configuration complete"

sleep 2 #settle down time
. $HOME/.profile
export PATH=/usr/local/bro/bin:$PATH
sleep 2 #settle down time

sudo /usr/local/bro/bin/broctl install

sudo systemctl enable logstash.service
sudo systemctl enable bro.service
sleep 2
sudo systemctl daemon-reload
sleep 2
sudo systemctl restart logstash.service
sleep 2
sudo systemctl restart bro.service
cd $HOME

git clone https://github.com/bro/package-manager.git
cd package-manager
sudo python setup.py install
sleep 2 #settle down time
cd $HOME
source ~/.profile

sudo env "PATH=$PATH" bro-pkg env
sudo env "PATH=$PATH" bro-pkg autoconfig
cd $HOME
