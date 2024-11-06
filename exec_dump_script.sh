#!/bin/bash

docker cp datadump.sh mysql:/datadump.sh
docker exec -it mysql bash -c "bash /datadump.sh"