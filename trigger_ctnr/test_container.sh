#! /bin/bash

repo_uri=$(cat repo_uri.info)

docker run -it \
	-e DB_CONN_STR=http://demo.kinetica.com:9191 \
	-e DB_USER=admin \
	-e DB_PASS=Kinetica1! \
    -e DB_SRC_TABLE=sensitivity_master \
	-e DB_DEST_TABLE=risk_inputs \
	-e FORCED_DELAY=3 \
	$repo_uri
