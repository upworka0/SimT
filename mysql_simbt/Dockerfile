FROM ideoconceptsca/mysql_dev
MAINTAINER Jeff Labonte "jflabonte@ideoconcepts.ca"

# Keep data persistent
VOLUME ["/var/lib/mysql"]

# Environment variables
ENV MYSQL_ROOT_PASSWORD Id30C0nc3pt5

COPY create_database.sql /docker-entrypoint-initdb.d/
