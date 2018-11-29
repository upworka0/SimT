#!/bin/bash

docker start mysql_dev
docker run --rm -ti -p 8000:8000 --name simbt_app --network simbt_network -v /home/jeff/Dropbox/Development/Projects/3E/3e201701_simbt_webapp_sw/simbt/:/code -e MYSQL_IP_ADDRESS=172.18.0.2 grimsleepless/simbt:1.0.3
