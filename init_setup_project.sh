#!/bin/bash
docker network rm simbt_network
docker stop mysql_dev
docker rm mysql_dev
docker stop simbt_app

DOCKER_REPO_NAME=ideoconceptsca

echo "Compilation des images Docker"
docker build -t $DOCKER_REPO_NAME/simbt .
cd mysql_simbt
docker build -t $DOCKER_REPO_NAME/mysql_simbt .

echo "Création du réseau pour SimBT"
docker network create simbt_network

echo "Démarrage de mysql pour la première fois"
docker volume create mysql_dev

docker run -d -p 3306:3306 --name mysql_dev --network simbt_network -mount src=mysql_dev,dst=/var/lib/mysql ${DOCKER_REPO_NAME}/mysql_simbt

cd ..
cd simbt
cd static
npm install

IP_ADDRESS=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql_dev)

echo "This is the MySQL Database IP Address withing Docker : ${IP_ADDRESS}"


