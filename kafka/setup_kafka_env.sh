#!/bin/bash
set -e
SRC_DIR="$(dirname $(readlink -f $0))"

echo "Command: $0 <kafka container name> <zookeeper client> <bootstrap server> <Options: [create|data_check|describe_group]>"
echo "Options: create [<topic name>|all] <partitions> <replication-factor>"
echo "Options: data_check <topic name>"
echo "Options: describe_group <group name>"

if [ $# -lt 5 ]
  then
    echo "$0 <kafka container name> <zookeeper client> <bootstrap server> <Options: [create|data_check|describe_group]>"
    echo "$0 kafka_kafka-1_1 localhost:22181 localhost:19092 create all 3 3"
    echo "$0 kafka_kafka-1_1 localhost:22181 localhost:19092 create bro_conn 3 3"
    echo "$0 kafka_kafka-1_1 localhost:22181 localhost:19092 data_check bro_conn"
    echo "$0 kafka_kafka-1_1 localhost:22181 localhost:19092 describe_group bro_conn"
    exit 1
fi

KAFKA_CONTAINER=$1
ZOOKEEPER_CLIENT=$2
BOOTSTRAP_SERVER=$3
OPTION=$4
PARAM1=$5
if [ $# -gt 5 ]
  then
    PARAM2=$6
    PARAM3=$7
fi
create_topic() {
  docker exec -u 0 $KAFKA_CONTAINER kafka-topics --create --topic $PARAM1 --partitions $PARAM2 --replication-factor $PARAM3 --if-not-exists --zookeeper $ZOOKEEPER_CLIENT
}

get_topic_data(){
  docker exec -u 0 $KAFKA_CONTAINER kafka-console-consumer --bootstrap-server $BOOTSTRAP_SERVER --topic $PARAM1
}

describe_topic(){
  docker exec -u 0 $KAFKA_CONTAINER kafka-consumer-groups --describe --group $PARAM1 --bootstrap-server $BOOTSTRAP_SERVER
}

case "$OPTION" in
create)
    if [ "$PARAM1" = "all" ]; then
      PARAM1="bro_conn"
      create_topic
      PARAM1="bro_ssl"
      create_topic
      PARAM1="bro_http"
      create_topic
      PARAM1="bro_x509"
      create_topic
      PARAM1="pipeline_0"
      create_topic
      PARAM1="ml_output"
      create_topic
    else
      create_topic
    fi
    ;;
data_check)
    get_topic_data
    ;;
describe_group)
    describe_topic
    ;;
*)
    echo "$0 ... $OPTION: unknown option"
    echo "Supported options: create data_check describe_group"
esac
