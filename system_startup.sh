#!/bin/bash

sudo service metricbeat restart
sudo service nginx restart
sudo service iptables-persistent restart
sudo service ssh restart
sudo iptables --policy FORWARD ACCEPT
sudo iptables --policy INPUT ACCEPT
echo "start jupyter hub from tmux shell manually"
