#!/bin/bash
set -e
SRC_DIR="$(dirname $(readlink -f $0))"

#export PATH=/home/sdn-nfv/anaconda3/envs/py35/bin:/home/sdn-nfv/bin:/home/sdn-nfv/.local/bin:/home/sdn-nfv/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin:$PATH
echo $PATH

cd $SRC_DIR/kafka/
docker-compose up -d
sleep 30

sudo sh setup_kafka_env.sh kafka_kafka-1_1 localhost:22181 localhost:19092 create all 3 3

cd $SRC_DIR/elk/
docker-compose up -d
sleep 30

cd $SRC_DIR/bro_dev/
docker-compose up -d
sleep 10


cd $SRC_DIR/data_processing_pipelines/example_1/
docker-compose up -d
sleep 10

cd $SRC_DIR/Clipper/experiments/experiment1/
#python simple_model_train_1.py
python simple_model_prod_1.py

cd $SRC_DIR/data_processing_pipelines/kafka_to_model/
docker-compose up -d
sleep 10


echo "docker ps"
docker ps

echo "docker images"
docker images

echo "deployment complete"
