#!/usr/bin/env python3
"""Create and start the containerized kafka connector for the fs demo."""
import os
import sys
import time

import json

import requests
import gpudb

from configs import credential_manifest
from configs import ingest_holdings_nightly, ingest_hist_volatility, ingest_security_master, ingest_market_tick_feed_byoc

target_ip = str(sys.argv[1])
print(f"Hitting KML API at {target_ip}")

kml_api_base = f'http://{target_ip}:9187/kml'

########################################################################################
# --- Start BYOC Exchange-Direct Ingestor
########################################################################################
r = requests.post(f'{kml_api_base}/ingest/create', json=ingest_market_tick_feed_byoc)
response_full = r.json()
i0 = response_full['response']['created']
ingest_id = i0['entity']['entity_id']
print(f'IEX Tick Stream Ingest created with ID: {ingest_id}')
start_resp = requests.get(f'{kml_api_base}/ingest/{ingest_id}/start').json()
print('Deployed...')


########################################################################################
# --- Start Kafka-Connector Ingest
########################################################################################

r = requests.post(f'{kml_api_base}/credential/create', json=credential_manifest).json()
cred_id = r['response']['created']['entity']['entity_id']
print(f'Kafka credential created with ID: {cred_id}')

ingest_holdings_nightly["ingest_config"]["cred_id"] = cred_id
ingest_hist_volatility["ingest_config"]["cred_id"] = cred_id
ingest_security_master["ingest_config"]["cred_id"] = cred_id

resp = requests.post(f'{kml_api_base}/ingest/create',
                     json=ingest_holdings_nightly).json()
resp = requests.post(f'{kml_api_base}/ingest/create',
                     json=ingest_hist_volatility).json()
resp = requests.post(f'{kml_api_base}/ingest/create',
                     json=ingest_security_master).json()





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