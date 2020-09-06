#!/bin/bash

set -x

echo "----------------------------------------"
echo "Running trigger script environment variables:"
echo "   DB_CONN_STR = $DB_CONN_STR"
echo "   DB_CONN_USER = $DB_CONN_USER"
echo "   DB_CONN_PASS = $DB_CONN_PASS"
echo "----------------------------------------"
echo ""

while true; do
    echo "fs-risk-trigger -- INFO -- (re)starting Trigger Script"

	python trigger_model.py \
	    --db-conn-str $DB_CONN_STR \
	    --db-conn-user $DB_USER \
	    --db-conn-pass $DB_PASS \
	    --db-src-table $DB_SRC_TABLE \
	    --db-dest-table $DB_DEST_TABLE \
	    --delay $FORCED_DELAY

    echo "fs-risk-trigger -- WARNING -- Trigger Script terminated"

    # HALT_AND_CATCH_FIRE
    sleep 5

done

echo "fs-risk-trigger -- ERROR -- Exiting shell"
