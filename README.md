# IDS_SYSTEM

## How to collaborate
* Fork the repo
* Make your changes.
* Push into your branch.
* Make a pull request to merge it in master


## Useful Commands

### Docker

- Docker compose commands:

  ```
  docker-compose up -d # start the container in background as per compose file
  docker-compose logs -ft # show logs for current compose file containers
  docker-compose <worker> exec -u 0 [command]
  docker-compose down -v # shutdown the cluster
  ```
- Docker execution commands

  `docker exec -u 0 <container id | container name> <command>`
- Get ip address of the container

  `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>`
- Run docker container from an image

  `docker run -it -u 0 --name <give container name> [-P] -p <host_port:container_port> -p <host_port:container_port> -e "<environment variable>" <docker image> <command to run>`
- list all docker images

  `docker images`

- see all containers

  `docker ps -a`

- '-p' to publish all exposed ports to random ports

  `docker run -it -P anurag1591/bro_ids /bin/bash`

- `docker pull anurag1591/bro_ids`

- remove all containers

  `docker rm $(docker ps -aq)`

- stop all containers

  `docker stop $(docker ps -aq)`

- remove all images  

  `docker rmi $(docker images -q)`

- Remove all stopped/exited containers

  `docker rm $(docker ps --filter "status=exited" -aq)`

- Remove images with none

  `docker rmi $(docker images -a | grep "^<none>" | awk '{print $3}')`

- List all containers

  `docker ps -aq`

- Show only stopped containers

  `docker ps --filter "status=exited"`

- Push images to docker cloud

  ```
  export DOCKER_ID_USER="anurag1591"
  docker login
  docker tag my_image $DOCKER_ID_USER/my_image
  docker push $DOCKER_ID_USER/my_image
  ```

- Build docker image from docker file

  `docker build -t anurag1591/bro_ids:1.1 -f /path/to/a/Dockerfile`

- Commit changes to docker images

  ```
  * sudo docker ps -l // get container id
  * sudo docker commit <container_id> new_image_name:tag_name(optional)
  * docker inspect <Commit hash> // View commit of using its hash
  ```
- restart it in the background

  `docker start f357e2faab77`

- reattach the terminal & stdin

  `docker attach f357e2faab77`

- Cleanup operations: These commands will remove all images and associated volumes. Do only if loss of data is okay.

  ```
  docker volume rm $(docker volume ls -qf dangling=true)
  docker system prune -a
  ```
- `docker-compose restart <worker>`


## How to run

* ssh sdn-nfv@130.65.157.239
- Start metricbeat

  `sudo service metricbeat restart`
- Start Nginx

  `sudo service nginx restart`
- Open Tmux shell

  `tmux`
- In the tmux shell, start Jupyter hub for pre existing workspace - lab

  ```
  cd ~/
  conda activate py35
  jupyter lab
  ```
- From a new terminal detach the tmux shell or attach to it again using:

  ```
  tmux detach
  tmux attach
  ```
- From your browser open jupiter notebook

  ```
  http://130.130.65.157.239/jupiterlab
  If prompted for password, use: jupiterlab
  ```
- Navigate to project directory
- Start the ids_system. Do not use sudo to start or stop the system. This will start the system in default setting.

  `sh start.sh`

- To stop use. This should do necessary cleanup operations:

  `sh stop.sh`

- Open kibana from browser

  `http://130.130.65.157.239/kibana`


## Navigate the repo

### __Kafka__

Create new topics. This assumes all 3 kafka nodes are up. Else it gives error.

  * Check if topic was created. Here topic name is bro_conn:

    `docker exec -u 0 kafka_kafka-1_1 kafka-topics --describe --topic bro_conn --zookeeper localhost:22181`
  * To check if topic is receiving data:

    `docker exec -u 0 kafka_kafka-1_1 kafka-console-consumer --bootstrap-server localhost:19092 --topic bro_conn --from-beginning --max-messages 3`
  * To create a consumer group:

    `docker exec -u 0 kafka_kafka-1_1 kafka-console-consumer --bootstrap-server localhost:19092 --topic bro_conn --from-beginning --consumer-property group.id=bro_conn_log`
  * Get group information:

    `docker exec -u 0 kafka_kafka-1_1 kafka-consumer-groups --bootstrap-server localhost:19092 --describe --group bro_conn_log`

  * Other commands :

    ```
    docker exec -u 0 kafka_kafka-1_1 kafka-consumer-groups --describe --group bro_conn_log --bootstrap-server localhost:19092
    ```
  - Use setup_kafka_env.sh to perform some basic operations

### __ELK cluster__:
Navigate to elk directory. Run this after kafka

* pip install elasticsearch-curator
  * Check verison , It should be 5.x to support Elasticsearch 6.4: `curator --version`
  * Create curator.yml and action.yml in ~/.curator directory. Check /elk/curator for these files.
  * `curator --dry-run action.yml` : This performs a dry run. Use it to see the possible outcome
  * `curator action.yml`
  * Other commands:

    ```
    curator_cli show_indices
    ```


### __Bro & Filebeat__
Navigate to bro_dev directory.
* restart Bro:

  ```
  docker exec -u 0 bro broctl install
  docker exec -u 0 bro broctl deploy
  ```
* start stop filebeat:

  ```
  docker exec -u 0 bro service filebeat stop
  docker exec -u 0 bro service filebeat start
  ```
* Assign filebeat.yml user:group as root and read write permission for all users

  ```
  sudo chown root:root etc/filebeat.yml
  sudo chmod -777 etc/filebeat.yml
  ```


### __Replay traffic__
I have already downloaded few pcaps. Replay using following commands. This will replay traffic on port where bro is logging.
* Navigate to: /Desktop/ids_system/packet_pusher/pcaps/
* execute: `sudo tcpreplay --mbps=200 --loop=100 --intf1=enp5s0f0 *`

### __NGINX__
This is required to access Kibana and Jupyter hub via browser

* To access Kibana: http://130.65.157.239/kibana
* To access Jupiterlab: http://130.65.157.239/jupiterlab
  * If prompted for a password, use jupiterlab
  * If prompter to use a differnt workspace, type your name and return.
* Refer ML/Jupiterlab for installation details
* Refer nginx/sites-available/default for proxy details

### __Jupiter Hub__
This is helpful for creating model pipeline and collaborative work
* Start tmux shell: Tmux allows to run jupyter in background. detach and attach to running tmux shell using, `tmux attach` and `tmux detach`
* From tmux shell
  ```
    conda activate py35 # This activates python 3.5 environment necessary for clipper.ai to work properly.
    conda deactivate
    jupyter lab
    [password: jupiterlab]
  ```
### Some other commands

- File transfer

  ```
  scp -r "/Users/sparta/Desktop/ids_system" sdn-nfv@130.65.157.239:/home/sdn-nfv/Desktop/ #from local machine to servr
  scp -r sdn-nfv@130.65.157.239:/home/sdn-nfv/Desktop/clipper_test.ipynb "/Users/sparta/Desktop/ids_system/Clipper/notebooks/" # from server to local machine
  ```
- Some other docker commands:

  ```
  docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.4.2

  docker run --name kibana -p 5601:5601 -e "ELASTICSEARCH_URL=http://172.17.0.2:9200" docker.elastic.co/kibana/kibana:6.4.2

  docker run -u 0 --name logstash -P -it --network host  docker.elastic.co/logstash/logstash:6.4.2 /bin/bash
  ```
* `ethtool -i enp5s0f1`
* Get the directories consuming disk space

  `sudo du -ma /var/lib/docker | sort -n -r | head -n 20`

* Get process blocking a port

  ```
  sudo netstat -nlp | grep :80
  ```


### Some links

* https://gist.github.com/Dev-Dipesh/2ac30a8a01afb7f65b2192928a875aa1

* https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-prod-cluster-composefile


### PF_RING support:

* Kernel installation:
  * https://www.ntop.org/pf_ring/installation-guide-for-pf_ring/
  * https://www.ntop.org/guides/pf_ring/get_started/git_installation.html
  * https://www.ntop.org/guides/pf_ring/vm_support/docker.html
* Zero copy: http://www.ntop.org/guides/pf_ring/zc.html
* With Bro: https://www.ntop.org/guides/pf_ring/thirdparty/bro.html
