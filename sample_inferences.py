import os
import sys
import traceback
import json
import copy
from pprint import pprint as pp

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

db = gpudb.GPUdb(encoding='BINARY',
                 host=DB_CONNECTION,
                 username='admin',
                 password='Kinetica1!')

sample_inf_req = {
    "img_uri": "https://terminator-vision.s3.amazonaws.com/scenic_drive.jpeg"
}

def helper_get_depl_id(dep_mode_sought):
    dep_list = requests.get(
        f"{REST_API}/kml/model/deployment/quicklist",
        auth=requests_cred
    ).json()

    relevant_depl_ids = []
    for d in dep_list["response"]["inventory"]:
        if (d['deployment_type'] == dep_mode_sought and
                d['entity_state'] == "RUNNING" and
                d['visibility'] != "ARCHIVED" and
                "Scenic Routing" in d["entity_name"]):                

                dp_id = d["entity_id"]
                relevant_depl_ids.append(dp_id)

    return relevant_depl_ids

def infer_on_demand():

    try:
        for dp_id in helper_get_depl_id(dep_mode_sought="ON_DEMAND"):
            print(f"Deployment {dp_id} is an active On-Demand "
                  f"Deployment, sending sample inference request")
            pp(sample_inf_req)
            inf_resp = requests.post(
                f"{REST_API}/kml/model/deployment/{dp_id}/infer",
                json=sample_inf_req,
                auth=requests_cred
            )
            print(f"Received inference response")

            inf_resp_j = inf_resp.json()
            assert inf_resp.status_code == 200, inf_resp_j
            assert "success" in inf_resp_j
            assert inf_resp_j["success"]
            assert "response" in inf_resp_j
            assert inf_resp_j["response"]

            assert "inference" in inf_resp_j["response"]
            assert inf_resp_j["response"]["inference"]
            
            assert len(inf_resp_j["response"]["inference"]) > 0
            for i in inf_resp_j["response"]["inference"]:
                pp(inf_resp_j["response"]["inference"][i])

    except Exception as e:
        print(e)
        print(traceback.format_exc())

def infer_continuous():

    try:
        for dp_id in helper_get_depl_id(dep_mode_sought="CONTINUOUS"):
            ctns_in_tbl = "road_images_inbounds"

            print(f"Deployment {dp_id} is an active Continuous "
                  f"Deployment, sending sample inference row inbounds into {ctns_in_tbl}")
            
            sink_table_h = gpudb.GPUdbTable(name=ctns_in_tbl, db=db)
            sink_table_h.insert_records(sample_inf_req)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


if __name__== "__main__":
    print("""\n
    ██╗  ██╗███╗   ███╗██╗         ██╗███╗   ██╗███████╗███████╗██████╗ 
    ██║ ██╔╝████╗ ████║██║         ██║████╗  ██║██╔════╝██╔════╝██╔══██╗
    █████╔╝ ██╔████╔██║██║         ██║██╔██╗ ██║█████╗  █████╗  ██████╔╝
    ██╔═██╗ ██║╚██╔╝██║██║         ██║██║╚██╗██║██╔══╝  ██╔══╝  ██╔══██╗
    ██║  ██╗██║ ╚═╝ ██║███████╗    ██║██║ ╚████║██║     ███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝╚═╝  ╚═══╝╚═╝     ╚══════╝╚═╝  ╚═╝
    """)  

    if "ON_DEMAND" in demo_environment["deployment_modes"]:
        infer_on_demand()
    if "CONTINUOUS" in demo_environment["deployment_modes"]:
        infer_continuous()
    
    # Batch inference is not required since it happens automatically upon deployment start
