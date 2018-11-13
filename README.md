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
* Remove all stopped/exited containers:
  * docker rm $(docker ps --filter "status=exited" -aq)
* Remove images with none
  * docker rmi $(docker images -a | grep "^<none>" | awk '{print $3}')
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
* Cleanup operations: These commands will remove all images and associated volumes. Do only if loss of data is okay.
  * docker volume rm $(docker volume ls -qf dangling=true)
  * docker system prune -a
## How to run

* ssh sdn-nfv@130.65.157.239
* Repo is in: Desktop/ids_system
* __Kafka__: Navigate to kafka directory. Start Kafka first
  * docker-compose up -d: wait till it starts
  * to view logs: docker-compose logs -f -t
  * Create new topics. Replace bro_conn with any topic name. Everything else is same. This assumes all 3 kafka nodes are up. Else it gives error. :
    * " docker exec -u 0 kafka_kafka-1_1 kafka-topics --create --topic bro_conn --partitions 3 --replication-factor 3 --if-not-exists --zookeeper localhost:22181 "
      * Create topics for: bro_conn, bro_ssl, bro_http, bro_intel, bro_x509
  * Check if topic was created. Here topic name is bro_conn:
    * docker exec -u 0 kafka_kafka-1_1 kafka-topics --describe --topic bro_conn --zookeeper localhost:22181
  * To check if topic is receiving data:
    * docker exec -u 0 kafka_kafka-1_1 kafka-console-consumer --bootstrap-server localhost:19092 --topic bro_conn --from-beginning --max-messages 3
  * To create a consumer group:
    * docker exec -u 0 kafka_kafka-1_1 kafka-console-consumer --bootstrap-server localhost:19092 --topic bro_conn --from-beginning --consumer-property group.id=bro_conn_log
  * Get group information:
    * docker exec -u 0 kafka_kafka-1_1 kafka-consumer-groups --bootstrap-server localhost:19092 --describe --group bro_conn_log
  * docker-compose down -v : To shutdown the cluster and remove the containers.
  * Kafka Commands:
    * docker exec -u 0 kafka_kafka-1_1 kafka-consumer-groups --describe --group bro_conn_log --bootstrap-server localhost:19092


* __ELK cluster__: Navigate to elk directory. Run this after kafka
  * docker-compose up -d: wait till it starts
  * to view logs: docker-compose logs -f -t
  * To access Kibana dashboard, from any browser go to: http://http://130.65.157.239/
  * docker-compose down: : To shutdown the cluster and remove the containers.
  * Install elasticsearch curator for indice deletion.
    * pip install elasticsearch-curator
      * Check verison : curator --version , It should be 5.x to support Elasticsearch 6.4
      * Create curator.yml and action.yml in ~/.curator directory. Check /elk/curator for these files.
      * curator --dry-run action.yml : This performs a dry run. Use it to see the possible outcome
      * curator action.yml
      * Other commands:
        * curator_cli show_indices
* __Bro & Filebeat__: Navigate to bro_dev directory.
  * docker-compose up -d: wait till it starts
  * to view logs: docker-compose logs -f -t
  * To open a shell to this container:
    * docker exec -it -u 0 bro /bin/bash
  * Get bro status: docker exec -u 0 bro broctl status
  * restart Bro:
    * docker exec -u 0 bro broctl install
    * docker exec -u 0 bro broctl deploy
  * start stop filebeat:
    * docker exec -u 0 bro service filebeat stop
    * docker exec -u 0 bro service filebeat start
  * Assign filebeat.yml user:group as root and read write permission for all users
    * sudo chown root:root etc/filebeat.yml
    * sudo chmod -777 etc/filebeat.yml
  * docker-compose down: : To shutdown the cluster and remove the containers.
* __Replay traffic__: I have already downloaded few pcaps. Replay using following commands. This will replay traffic on port where bro is logging.
  * Navigate to: /Desktop/ids_system/packet_pusher/pcaps/
  * execute: sudo tcpreplay --mbps=200 --loop=100 --intf1=enp5s0f1 *
  * sudo tcpreplay --pps=10000 --loop=100 --intf1=enp5s0f1 *
* __NGINX__ : This is required to access Kibana and Jupiterlab via browser
  * To access Kibana: http://130.65.157.239/kibana
  * To access Jupiterlab: http://130.65.157.239/jupiterlab
    * If prompted for a password, use jupiterlab
    * If prompter to use a differnt workspace, type your name and return.
  * Refer ML/Jupiterlab for installation details
  * Refer nginx/sites-available/default for proxy details
* __Jupiter Hub__: This is helpful for creating model pipeline and collaborative work
  * conda activate py35: This activates python 3.5 environment necessary for clipper.ai to work properly.
  * conda deactivate
  * jupyter lab: [password: jupiterlab]

## Some other commands

* scp -r "/Users/sparta/Desktop/ids_system" sdn-nfv@130.65.157.239:/home/sdn-nfv/Desktop/
* scp -r sdn-nfv@130.65.157.239:/home/sdn-nfv/Desktop/clipper_test.ipynb "/Users/sparta/Desktop/ids_system/Clipper/notebooks/" 
* docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id
* sudo rm -rf kafka-1/data/* & sudo rm -rf kafka-2/data/* & sudo rm -rf kafka-3/data/*
* sudo rm -rf zookeeper-1/data/* & sudo rm -rf zookeeper-1/log/* & sudo rm -rf zookeeper-2/data/* & sudo rm -rf zookeeper-2/log/* & sudo rm -rf zookeeper-3/data/* & sudo rm -rf zookeeper-3/log/*
* docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.4.2
* docker run --name kibana -p 5601:5601 -e "ELASTICSEARCH_URL=http://172.17.0.2:9200" docker.elastic.co/kibana/kibana:6.4.2
* docker run -u 0 --name logstash -P -it --network host  docker.elastic.co/logstash/logstash:6.4.2 /bin/bash
* ethtool -i enp5s0f1
* service nginx start
* du -ma /var/lib/docker | sort -n -r | head -n 20
* kafka version: docker logs kafka_kafka-1_1 | egrep -i "kafka\W+version"


## Some links

* https://gist.github.com/Dev-Dipesh/2ac30a8a01afb7f65b2192928a875aa1

* https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-prod-cluster-composefile


## PF_RING support:

* Kernel installation:
  * https://www.ntop.org/pf_ring/installation-guide-for-pf_ring/
  * https://www.ntop.org/guides/pf_ring/get_started/git_installation.html
  * https://www.ntop.org/guides/pf_ring/vm_support/docker.html
* Zero copy: http://www.ntop.org/guides/pf_ring/zc.html
* With Bro: https://www.ntop.org/guides/pf_ring/thirdparty/bro.html
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
