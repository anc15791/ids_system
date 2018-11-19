#!/bin/bash

curator ~/.curator/action.yml
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -qf dangling=true)
docker system prune -a < yes
