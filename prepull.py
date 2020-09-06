#!/usr/bin/env python3

import os
import sys
import time

import json

import requests
import gpudb

from configs import demo_environment

# ---------------------------------------------
# Environment details and credentials
REST_API = demo_environment["rest_api"]
DB_USER = demo_environment["db_user"]
DB_PASSWORD = demo_environment["db_password"]
requests_cred = None
if DB_USER and DB_PASSWORD:
    requests_cred = (DB_USER, DB_PASSWORD)
else:
    requests_cred = None
# ---------------------------------------------

pre_pullable_containers = [
  "kinetica/ctnr-kml-bbox-ml-deep-img-segment-gpu:r7.1.1"
  ,"kinetica/ctnr-kml-byoc-kinesis-photoapp:r7.1.0"
  ,"kinetica/ctnr-kml-byoc-sample-mapillary:r7.1.0"
  ,"kinetica/ctnr-kml-bbox-ml-deep-img-segment-gpu:r7.1.0"
  ]

for pp in pre_pullable_containers:
  r = requests.post(f'{REST_API}/kml/admin/cluster/prepull',
                  json={"container_ref": pp},
                  timeout=7200,
                  auth=requests_cred)
  print(r.status_code)
  print(r.text)
