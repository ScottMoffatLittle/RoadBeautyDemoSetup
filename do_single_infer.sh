#!/bin/sh

# Sample inference

curl -vX POST http://demo.kinetica.com:9187/kml/model/deployment/169/infer \
-d @sample_inf_payload.json \
--header "Content-Type: application/json" | json_pp