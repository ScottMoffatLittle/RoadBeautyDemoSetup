import os
import sys
import json
import pprint

import requests
import gpudb

from configs import (
    demo_environment,
    model_inst_cfg__img_segment,
    model_dep_cfg__img_segment_ondem,
    model_dep_cfg__img_segment_ctns,
    model_dep_cfg__img_segment_batch
)

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

print(f"Connecting to DB: {DB_CONNECTION}")

db = gpudb.GPUdb(encoding='BINARY',
                 host=DB_CONNECTION,
                 username='admin',
                 password='Kinetica1!')


def deploy_model(dep_create_payload):
    mi_create_response = requests.post(
        f'{REST_API}/kml/model/instance/create',
        json=model_inst_cfg__img_segment,
        auth=requests_cred
    )
    mi0 = mi_create_response.json()
    mi_id = mi0['response']['created']['entity']['entity_id']
    print(f'Created BlackBox Model Instance with ID {mi_id}')

    print('Creating Model Deployment')
    
    md_create_response = requests.post(
        f'{REST_API}/kml/model/instance/{mi_id}/deploy',
        json=dep_create_payload,
        auth=requests_cred
    )
    assert md_create_response.status_code == 201, md_create_response.json()

    md_create_response_j = md_create_response.json()
    md_id = md_create_response_j['response']['created']['entity']['entity_id']

    print("Starting deployment")
    md_start_response = requests.get(
        f'{REST_API}/kml/model/deployment/{md_id}/start',
        auth=requests_cred
    )
    assert md_start_response.status_code == 200, md_start_response.json()

    return md_id
    
def main():
    print("*"*50)
    print(f'Targeting Environment {REST_API}')
    print("\n")
    print("*"*50)
    print("Environment Details")
    env_info_resp = requests.get(f"{REST_API}/kml/ping", auth=requests_cred)
    assert env_info_resp.json()["success"], env_info_resp.json()

    print(f"Deployment mode targets: {demo_environment['deployment_modes']}")
    if "ON_DEMAND" in demo_environment["deployment_modes"]:
        print("\n\nDeploying in on-demand mode...")
        md_id = deploy_model(dep_create_payload=model_dep_cfg__img_segment_ondem)
        print(f"\tModel Deployed Successfully with ID: {md_id}")
    if "CONTINUOUS" in demo_environment["deployment_modes"]:
        print("\n\nDeploying in continuous mode...")
        md_id = deploy_model(dep_create_payload=model_dep_cfg__img_segment_ctns)
        print(f"\tModel Deployed Successfully with ID: {md_id}")
    if "BATCH" in demo_environment["deployment_modes"]:        
        print("\n\nDeploying in batch mode...")
        md_id = deploy_model(dep_create_payload=model_dep_cfg__img_segment_batch)
        print(f"\tModel Deployed Successfully with ID: {md_id}")


if __name__ == "__main__":

    print("""\n
    ██╗  ██╗███╗   ███╗██╗         ██████╗ ███████╗███╗   ███╗ ██████╗     ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
    ██║ ██╔╝████╗ ████║██║         ██╔══██╗██╔════╝████╗ ████║██╔═══██╗    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
    █████╔╝ ██╔████╔██║██║         ██║  ██║█████╗  ██╔████╔██║██║   ██║    ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
    ██╔═██╗ ██║╚██╔╝██║██║         ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
    ██║  ██╗██║ ╚═╝ ██║███████╗    ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝    ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
    ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝     ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
    """)
    main()
