#!/bin/bash

docker cp datadump.sh mysql:/datadump.sh
docker exec -it mysql bash -c "bash /datadump.sh"
docker cp mysql:/sales_data.sql sales_data.sql

docker cp catalog.json mongodb:/catalog.json
docker exec -it mongodb bash -c "mongoimport --db catalog --collection electronics --file catalog.json -u root -p mysecretpassword --authenticationDatabase admin"

docker exec -it mongodb bash -c "mongoexport --host localhost --port 27017 -u root -p mysecretpassword --authenticationDatabase admin --db catalog --collection electronics --type=csv --fields _id,type,model --out electronics.csv"
docker cp mongodb:/electronics.csv electronics.csv