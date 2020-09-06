import os
import sys
import copy
import collections
import uuid
import json
import time
import copy
import random
import pprint
from random import randint

import requests
import gpudb

from configs import *

CONTAINER_MODEL = "kinetica/ctnr-kml-bbox-ml-deep-img-segment-cpu:r7.1.0"
CONTAINER_INGEST = "kinetica/ctnr-kml-bbox-ml-deep-img-segment-cpu:r7.1.0"

# modify for target machine and database installation
TARGET_REST_API_IP = sys.argv[1]
TARGET_DATABASE_IP = sys.argv[2]

DB_USER = "admin"
DB_PASS = "Kinetica1!"

db_conn = f'http://{TARGET_DATABASE_IP}:9191'
api_conn = f'http://{TARGET_REST_API_IP}:9187'

requests_cred = None
if DB_USER and DB_PASS:
    requests_cred = (DB_USER, DB_PASS)
    db = gpudb.GPUdb(encoding='BINARY',
                     host=db_conn,
                     username=DB_USER,
                     password=DB_PASS)
else:
    requests_cred = None
    db = gpudb.GPUdb(encoding='BINARY',
                 host=db_conn)

def setup_demo_batch(model_inst_config, api_base):
    mi_create_response = requests.post(f'{api_base}/model/instance/create', 
        json={
            "model_inst_name":"Road beauty",
            "model_inst_desc":"Road beauty",
            "model_inst_config": model_inst_config
            }, auth=requests_cred)
    mi0 = mi_create_response.json()
    print(mi0)
    mi_id = mi0['response']['created']['entity']['entity_id']
    print(f'Created BlackBox Model Instance with ID {mi_id}')

    in_spec_deployment = {'REPLICAS': 1,
                          'deployment_mode': 'BATCH',
                          'source_table': 'demo_road_beauty',
                          'sink_table': 'demo_road_beauty_inferenced',
                          'deployment_name': 'asdfasdf',
                          'deployment_desc': 'sdfasdf'}    
    print('\tDeploying model...')        
    md_create_response = requests.post(f'{api_base}/model/instance/{mi_id}/deploy',
                                       json=in_spec_deployment, auth=requests_cred)
    md = md_create_response.json()
    md_id = md['response']['created']['entity']['entity_id']

    md_create_response = requests.post(f'{api_base}/model/deployment/{md_id}/start',
                                       json=in_spec_deployment, auth=requests_cred)

    return (md_id, in_spec_deployment['sink_table'])

def main():

    print("*"*50)
    KML_API_BASE = f'{api_conn}/kml'
    print(f'Targeting Environment {KML_API_BASE}')

    print("\n")
    print("*"*50)
    print("Environment Details")
    env_info_resp = requests.get(f"{KML_API_BASE}/ping", auth=requests_cred)
    pprint.pprint(env_info_resp)

    model_inst_config = {

    }

    print('Preparing demo for Mode: CONTINUOUS')
    (dep_id_ct, out_tbl_ct) = setup_demo_batch(model_img_segment, KML_API_BASE)
    print(f'\tInferenced in Continuous-Mode on model Deployment ID {dep_id_ct}')
    print(f'\tPlaced results at {out_tbl_ct}')
    
    print('Models Deployed ...')
    
if __name__ == "__main__":
    main()
