import os
import sys
import traceback
import json
from pprint import pprint as pp

import requests
import gpudb

from configs import demo_environment
from configs import CLEANSE_WORTHY_CONTAINERS
from configs import CLEANSE_WORTHY_INGESTS
from configs import CLEANSE_WORTHY_FEATURESETS

# ---------------------------------------------
# Environment details and credentials
REST_API = demo_environment["rest_api"]
DB_CONN_STR = demo_environment["db_connection"]
DB_USER = demo_environment["db_user"]
DB_PASSWORD = demo_environment["db_password"]
requests_cred = None
if DB_USER and DB_PASSWORD:
    requests_cred = (DB_USER, DB_PASSWORD)
else:
    requests_cred = None
# ---------------------------------------------


def main():

    try:

        archiveable_models = []
        mdl_list = requests.get(
            f"{REST_API}/kml/model/instance/quicklist",
            auth=requests_cred
        ).json()
        for m in mdl_list["response"]["inventory"]:
            
            if m['model_inst_config']['container'].split(":")[0] in CLEANSE_WORTHY_CONTAINERS:
                archiveable_models.append(m['entity_id'])
                if m['visibility'] != 'ARCHIVED':
                    print(f"  Being Archived: Model {m['entity_id']}: "
                          f"{m['entity_name']}")
                    _ = requests.get(
                        f"{REST_API}/kml/model/instance/{m['entity_id']}/archive",
                        auth=requests_cred
                    )
                else:
                    print(f"  Already Archived: Model {m['entity_id']}: "
                          f"{m['entity_name']}")

        dep_list = requests.get(
            f"{REST_API}/kml/model/deployment/quicklist",
            auth=requests_cred
        ).json()

        for d in dep_list["response"]["inventory"]:
            if d['base_model_inst_id'] in archiveable_models:
                if d['entity_state'] != 'STOPPED':
                    print(f"  Being Terminated: Deployment {d['entity_id']} "
                          f"being terminated: {d['entity_name']}")
                    _ = requests.get(
                        f"{REST_API}/kml/model/deployment/{d['entity_id']}/stop",
                        auth=requests_cred
                    )
                else:
                    print(f"  Already Terminated: Deployment {d['entity_id']} "
                          f"already terminated: {d['entity_name']}")

                if d['visibility'] != 'ARCHIVED':
                    print(f"  Being Archived: Deployment {d['entity_id']}: "
                          f"{d['entity_name']}")
                    _ = requests.get(
                        f"{REST_API}/kml/model/deployment/{d['entity_id']}/archive",
                        auth=requests_cred
                    )
                else:
                    print(f"  Already Archived: Deployment {d['entity_id']}: "
                          f"{d['entity_name']}")

        ingest_list = requests.get(
            f"{REST_API}/kml/ingest/quicklist",
            auth=requests_cred
        ).json()

        for d in ingest_list["response"]["inventory"]:
            for cwi in CLEANSE_WORTHY_INGESTS:
                if cwi in d['entity_name']:
                
                    if d['entity_state'] != 'TERMINATED':
                        print(f"  Being Terminated: Ingest {d['entity_id']}: "
                              f"{d['entity_name']}")
                        _ = requests.get(
                            f"{REST_API}/kml/ingest/{d['entity_id']}/terminate",
                            auth=requests_cred
                        )
                    else:
                        print(f"  Already Terminated: Ingest {d['entity_id']}: "
                              f"{d['entity_name']}")

                    if d['visibility'] != 'ARCHIVED':
                        print(f"  Being Archived: Ingest {d['entity_id']}: "
                              f"{d['entity_name']}")
                        _ = requests.get(
                            f"{REST_API}/kml/ingest/{d['entity_id']}/archive",
                            auth=requests_cred
                        )
                    else:
                        print(f"  Already Archived: Ingest {d['entity_id']}: "
                              f"{d['entity_name']}")


                    try:
                        if DB_USER and DB_PASSWORD:
                            db = gpudb.GPUdb(host=DB_CONN_STR, username=DB_USER, password=DB_PASSWORD)
                        else:
                            db = gpudb.GPUdb(host=DB_CONN_STR)

                        status = db.delete_records(table_name="sys_kml_entity", expressions=["entity_type='INGEST'"])
                        print(status)
                        status = db.delete_records(table_name="sys_kml_ingest", expressions=["entity_id>0"])
                        print(status)
                    except Exception as ee:
                        print(ee)


        fs_list = requests.get(
            f"{REST_API}/kml/featureset/quicklist",
            auth=requests_cred
        ).json()
        for f in fs_list["response"]["inventory"]:
            for cwn in CLEANSE_WORTHY_FEATURESETS:
                if cwn in f['entity_name']:
                    if f['visibility'] != 'ARCHIVED':
                        print(f"  Being Archived: FeatureSet {f['entity_id']}: "
                              f"{f['entity_name']}")
                        _ = requests.get(
                            f"{REST_API}/kml/featureset/{f['entity_id']}/archive",
                            auth=requests_cred
                        )
                    else:
                        print(f"  Already Archived: FeatureSet {f['entity_id']}: "
                              f"{f['entity_name']}")

    except Exception as e:
        print(e)
        print(traceback.format_exc())


if __name__== "__main__":

    print("""\n
    ██╗  ██╗███╗   ███╗██╗         ████████╗██╗██████╗ ██╗   ██╗
    ██║ ██╔╝████╗ ████║██║         ╚══██╔══╝██║██╔══██╗╚██╗ ██╔╝
    █████╔╝ ██╔████╔██║██║            ██║   ██║██║  ██║ ╚████╔╝ 
    ██╔═██╗ ██║╚██╔╝██║██║            ██║   ██║██║  ██║  ╚██╔╝  
    ██║  ██╗██║ ╚═╝ ██║███████╗       ██║   ██║██████╔╝   ██║   
    ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝       ╚═╝   ╚═╝╚═════╝    ╚═╝   
    """)
    main()
