#! /bin/bash
set -ex

export DB_CONN_STR=http://demo.kinetica.com:9191
export DB_USER=admin
export DB_PASS=Kinetica1!
export DB_SRC_TABLE=sensitivity_master
export DB_DEST_TABLE=risk_inputs
export FORCED_DELAY=3

./trigger_model.sh
