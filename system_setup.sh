#!/bin/bash

sudo apt-get update
sudo apt-get install -y iptables-persistent openssh-server tmux nginx wget default-jre default-jvm
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A FORWARD -p tcp --dport 22 -j ACCEPT
sudo iptables -A FORWARD -p tcp --dport 80 -j ACCEPT
sudo iptables --policy FORWARD ACCEPT
sudo iptables --policy INPUT ACCEPT
sudo iptables --policy OUTPUT ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda create -n py35 python=3.5
conda env create -f environment.yml
conda list
