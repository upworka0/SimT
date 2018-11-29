#!/bin/bash

cat /code/simbt/settings.py | sed "s|172.18.0.2|$MYSQL_IP_ADDRESS|" > /code/new_settings.py \
  && mv /code/new_settings.py /code/simbt/settings.py

python /code/manage.py runserver 0.0.0.0:8000
