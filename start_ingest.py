#!/usr/bin/env python3
"""Create and start the containerized kafka connector for the fs demo."""
import os
import sys
import time

import json

import requests
import gpudb

from configs import credential_manifest
from configs import demo_environment
from configs import ingest_photostream_app_kafka_kinesis
from configs import ingest_photostream_byoc_mapillarry

# ---------------------------------------------
# Environment details and credentials
REST_API = demo_environment["rest_api"]
DB_CONNECTION = demo_environment["db_connection"]
DB_USER = demo_environment["db_user"]
DB_PASSWORD = demo_environment["db_password"]
requests_cred = None
if DB_USER and DB_PASSWORD:
    requests_cred = (DB_USER, DB_PASSWORD)
else:
    requests_cred = None
# ---------------------------------------------

kml_api_base = demo_environment["rest_api"]
print(f"Starting ingests at {kml_api_base}")

########################################################################################
# --- Start BYOC Mapilarry Ingestor
########################################################################################
r = requests.post(f'{kml_api_base}/kml/ingest/create', 
                  json=ingest_photostream_byoc_mapillarry,
                  auth=requests_cred)
response_full = r.json()
i0 = response_full['response']['created']
ingest_id = i0['entity']['entity_id']
print(f'Mapillarry Ingest created with ID: {ingest_id}')
start_resp = requests.get(f'{kml_api_base}/kml/ingest/{ingest_id}/start',
                          auth=requests_cred).json()
print('Deployed...')


########################################################################################
# --- Start Kafka-Connector Ingest
########################################################################################

r = requests.post(f'{kml_api_base}/kml/ingest/create', 
                  json=ingest_photostream_app_kafka_kinesis,
                  auth=requests_cred)
response_full = r.json()
i0 = response_full['response']['created']
ingest_id = i0['entity']['entity_id']
print(f'Amazon AWS Kinesis Ingestor for Kinetica Photo Snap-App: {ingest_id}')
start_resp = requests.get(f'{kml_api_base}/kml/ingest/{ingest_id}/start', 
                          auth=requests_cred).json()
print('Deployed...')





########################################################################################
# --- Start Kafka-Connector Ingest
########################################################################################

'''
target_table = 'iex_stream'
topic = 'stocks7'
kafka_ip = 'kafka.kinetica.com'
kafka_port = '9092'

keystore_pass = ''
keystore = ''

# Create credentials object
print('creating credentials')
cred_spec = {'credential_name': 'Trade activity stream',
             'credential_desc': 'Credentials for FinServ ingest',
             'credential_type': 'KAFKA',
             'credential_config': {'connection_str': f'{kafka_ip}:{kafka_port}',
                                   'topics': topic,
                                   'keystore': keystore,
                                   'key_password': keystore_pass}}

r = requests.post(f'{kml_api_base}/credential/create', data=json.dumps(cred_spec)).json()
cred_id = r['response']['created']['entity']['entity_id']
print(f'Kafka credential created with ID: {cred_id}')

# Create ingest
print('starting ingest')
test_args = {'target_table': target_table,
             'source': 'kafka',
             'cred_id': cred_id}

response_full = requests.post(f'{kml_api_base}/ingest/create',
                              data=json.dumps({'ingest_name': 'IEX Live Market Trading Stream',
                                               'ingest_desc': 'Live stock market trading activity',
                                               'ingest_mode': 'CONTINUOUS',
                                               'ingest_type': 'KAFKA',
                                               'ingest_config': test_args})).json()
i0 = response_full['response']['created']
ingest_id = i0['entity']['entity_id']
print(f'Kafka Ingest created with ID: {ingest_id}')
# Start the Kafka-Kinetica connector
start_resp = requests.get(f'{kml_api_base}/ingest/{ingest_id}/start').json()
print('Deployed...')
'''