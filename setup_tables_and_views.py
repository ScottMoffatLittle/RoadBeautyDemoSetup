#!/usr/bin/env python3

import os
import sys
import time
import pprint
import json
import collections
import random
import csv

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

def main():

    print(f"Connecting to DB: {DB_CONNECTION}")

    db = gpudb.GPUdb(encoding='BINARY',
                     host=DB_CONNECTION,
                     username='admin',
                     password='Kinetica1!')

    create_sqls = [
        "tbl_create/road_images_bulkloaded.sql",
        "tbl_create/road_images_inbounds.sql"
        ]

    for sql_file in create_sqls:
        with open(sql_file, 'r') as f:
            sql = f.read()
        status = db.execute_sql(sql)
        #print(status)

    load_queue = [
          ("demo_scenic_routing.road_images_bulkloaded", "data/bulk_loaded_road_images.csv"),
          ]

    for (sink_table_name, source_file) in load_queue:
        print(f"Loading data file {source_file} into table {sink_table_name}")
        print("\tReading file...")
        with open(source_file, mode='r') as f:
            fullfile = list(csv.reader(f))
            hdr = fullfile[0]
            datalines = fullfile[1:]
            insert_queue = [{hdr[c]:aline[c] for c in range(len(hdr))} for aline in datalines]        
        print("\tInserting into DB...")
        sch, nm = sink_table_name.split(".")
        sink_table_h = gpudb.GPUdbTable(name=nm, db=db)
        sink_table_h.insert_records(insert_queue)

if __name__ == "__main__":
    main()
