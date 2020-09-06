#!/bin/bash

set -ex 

echo "Cleaning up any existing deployments"
python ./tidy.py

echo "Pre-pull containers"
python ./prepull.py

#echo "Setting up required tables"
#python ./setup_tables_and_views.py

echo "Running Ingests"
python ./start_ingest.py
sleep 30

python ./start_models.py
echo "Waiting for spinup"
sleep 30


#echo "Populating sample inferences"
#python ./sample_inferences.py
