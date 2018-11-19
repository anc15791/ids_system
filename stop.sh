#!/bin/bash
set -e
SRC_DIR="$(dirname $(readlink -f $0))"

#export PATH=/home/sdn-nfv/anaconda3/envs/py35/bin:/home/sdn-nfv/bin:/home/sdn-nfv/.local/bin:/home/sdn-nfv/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin:$PATH
echo $PATH

cd $SRC_DIR/kafka/
docker-compose down -v

cd $SRC_DIR/elk/
docker-compose down -v

cd $SRC_DIR/bro_dev/
docker-compose down -v


cd $SRC_DIR/data_processing_pipelines/example_1/
docker-compose down -v

cd $SRC_DIR/data_processing_pipelines/kafka_to_model/
docker-compose down -v

cd $SRC_DIR/Clipper/experiments/
python stop.py

echo "docker ps"
docker ps

echo "remove all containers"
docker rm $(docker ps -aq)

echo "remove images tagged as none. Mostly due to using same name/version of a model"
docker rmi $(docker images -a | grep "^<none>" | awk '{print $3}')

echo "docker images"
docker images
echo "removal complete"
