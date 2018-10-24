#!/bin/bash
export PATH=$PATH:/usr/local/bro/bin
broctl install
broctl deploy
service filebeat start
