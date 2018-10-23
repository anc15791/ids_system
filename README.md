# Smart Intrusion detection system

## How to collaborate
* Fork the repo
* Make your changes.
* Push into your branch.
* Make a pull request to merge it in master

## Navigation


## Useful Docker Commands

* docker images
  *
* docker ps -a: see all containers
* docker run -it -P anurag1591/bro_ids /bin/bash : -p to publish all exposed ports to random ports
* docker pull anurag1591/bro_ids
* docker rm $(docker ps -aq) : remove all containers
* docker stop $(docker ps -aq) : stop all containers
* docker rmi $(docker images -q) : remove all images
* docker ps -aq : List all containers
* docker ps --filter "status=exited" : Show only stopped containers
* Push images to docker cloud
  * export DOCKER_ID_USER="anurag1591"
  * docker login
  * docker tag my_image $DOCKER_ID_USER/my_image
  * docker push $DOCKER_ID_USER/my_image
* Build docker image from docker file
  * docker build -t anurag1591/bro_ids:1.1 -f /path/to/a/Dockerfile .
* Commit changes to docker images
  * sudo docker ps -l : get container id
  * sudo docker commit <container_id> new_image_name:tag_name(optional)
  * docker inspect <Commit hash> : View commit of using its hash
* docker start f357e2faab77 # restart it in the background
* docker attach f357e2faab77 # reattach the terminal & stdin

## How to run

* ssh sdn-nfv@130.65.157.239
* Repo is in: Desktop/ids_system
* __Kafka__: Navigate to kafka directory. Start Kafka first
  * docker-compose up : wait till it starts
  * Create new topics. Replace bro_conn with any topic name. Everything else is same. This assumes all 3 kafka nodes are up. Else it gives error. :
    * " docker exec -u 0 kafka_kafka-1_1 kafka-topics --create --topic bro_conn --partitions 3 --replication-factor 3 --if-not-exists --zookeeper localhost:22181 "
  * Check if topic was created. Here topic name is bro_conn:
    * docker exec -u 0 kafka_kafka-1_1 kafka-topics --describe --topic bro_conn --zookeeper localhost:22181
  * To check if topic is receiving data:
    * docker exec -u 0 kafka_kafka-1_1 kafka-console-consumer --bootstrap-server localhost:19092 --topic bro_conn --from-beginning --max-messages 3
  * docker-compose down: : To shutdown the cluster and remove the containers.

* __ELK cluster__: Navigate to elk directory. Run this after kafka
  * docker-compose up : wait till it starts.
  * To access Kibana dashboard, from any browser go to: http://http://130.65.157.239/
  * docker-compose down: : To shutdown the cluster and remove the containers.
* __Bro & Filebeat__: This container is already running. DO NOT STOP IT. Bro and Filebeat are working and doing their job.
  * To open a shell to this container:
    * docker exec -it -u 0 bro /bin/bash
    * restart Bro:
      * broctl install
      * broctl deploy
    * start stop filebeat:
      * service filebeat stop
      * service filebeat start
* __Replay traffic__: I have already downloaded few pcaps. Replay using following commands. This will replay traffic on port where bro is logging.
  * Navigate to: /Desktop/ids_system/packet_pusher/pcaps/
  * execute: sudo tcpreplay --intf1=eno1 *


## Some other commands

* scp -r "/Users/sparta/Desktop/ids_system" sdn-nfv@130.65.157.239:/home/sdn-nfv/Desktop/

* docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id

* sudo rm -rf kafka-1/data/* & sudo rm -rf kafka-2/data/* & sudo rm -rf kafka-3/data/*

* sudo rm -rf zookeeper-1/data/* & sudo rm -rf zookeeper-1/log/* & sudo rm -rf zookeeper-2/data/* & sudo rm -rf zookeeper-2/log/* & sudo rm -rf zookeeper-3/data/* & sudo rm -rf zookeeper-3/log/*

* docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.4.2

* docker run --name kibana -p 5601:5601 -e "ELASTICSEARCH_URL=http://172.17.0.2:9200" docker.elastic.co/kibana/kibana:6.4.2

* docker run -u 0 --name logstash -P -it --network host  docker.elastic.co/logstash/logstash:6.4.2 /bin/bash


## Some links

* https://gist.github.com/Dev-Dipesh/2ac30a8a01afb7f65b2192928a875aa1

* https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-prod-cluster-composefile


## Misc
-----------------------------------------------
KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
KAFKA_DEFAULT_REPLICATION_STATUS: 3
SERVER_DEFAULT_REPLICATION_STATUS: 3
DEFAULT_REPLICATION_FACTOR: 3
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
SERVER_OFFSETS_TOPIC_REPLICATION_FACTOR: 3

volumes:
  - ./persistent_mount/zookeeper-1/data:/var/lib/zookeeper/data
  - ./persistent_mount/zookeeper-1/log:/var/lib/zookeeper/log

  volumes:
    - ./persistent_mount/kafka-1/data:/var/lib/kafka/data
-----------------------------------------------
logstash-plugin install logstash-output-kafka
