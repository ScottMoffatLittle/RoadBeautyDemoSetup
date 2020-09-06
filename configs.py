##############################################################################
# MODEL SETUP
##############################################################################

demo_environment = {
    "rest_api":      "http://172.31.32.32:9187",
    "db_connection": "http://172.31.32.32:9191",
    "db_user": "admin",
    "db_password": "Kinetica1!",
    "deployment_modes": ["CONTINUOUS"]
}

CLEANSE_WORTHY_CONTAINERS = [
    "kinetica/ctnr-kml-bbox-ml-deep-img-segment-gpu",
    "kinetica/ctnr-kml-bbox-ml-deep-img-segment-cpu",
    "kinetica/ctnr-kml-bbox-ml-deep-img-segment"
]

CLEANSE_WORTHY_INGESTS = [
    "Mapillary",
    "KineticaCam",
    "Scenic Routing",
    "Road Footage"
]

CLEANSE_WORTHY_FEATURESETS = [
    "Mapillary",
    "Beauty",
    "Scenic Routing",
    "Dashcam"
]

model_inst_cfg__img_segment = {
    "model_inst_name": "Image Scene Semantic Segmenter using PyTorch",
    "model_inst_desc": "Image Scene Semantic Segmenter using PyTorch",
    "model_inst_config": {
        "model_type": "BLACKBOX",
        "container": "kinetica/ctnr-kml-bbox-ml-deep-img-segment-gpu:r7.1.1",
        "bb_module": "bb_module_default",
        "bb_function": "segment_pct_img_from_uri",
        "blackbox_module": "bb_module_default",
        "blackbox_function": "segment_pct_img_from_uri",
        "input_record_type": [
            {
                "col_name": "img_uri",
                "col_type": "string|char128",
            }
        ],
        "output_record_type": [
            {
                "col_name": "item_pct",
                "col_type": "double",
            },
            {
                "col_name": "item_class",
                "col_type": "string|char32",
            }
        ]
    }
}

model_dep_cfg__img_segment_ondem = {
    'replicas': 1,
    'compute_target': "GPU",
    'gpu_compute_target_allocation': 1,
    'deployment_mode': 'ON_DEMAND',
    'deployment_name': 'Scenic Routing',
    'deployment_desc': 'Scenic Routing'
}

model_dep_cfg__img_segment_ctns = {
    'replicas': 1,
    'compute_target': "GPU",
    'gpu_compute_target_allocation': 1,
    'deployment_mode': 'CONTINUOUS',
    'deployment_name': 'Scenic Routing',
    'deployment_desc': 'Scenic Routing',
    'source_table': "dashcam_snapapp_inbounds",
    "sink_table": 'dashcam_snapapp_beauty_scored'
}

model_dep_cfg__img_segment_batch = {
    'replicas': 4,
    'compute_target': "GPU",
    'gpu_compute_target_allocation': 1,
    'deployment_mode': 'BATCH',
    'deployment_name': 'Scenic Routing',
    'deployment_desc': 'Scenic Routing',
    'source_table': "road_images_inbounds_mapillary_bkny",
    "sink_table": 'road_images_scored_batch'
}

model_inst_cfg__greeniness = {}
model_dep_cfg__greeniness = {}

##############################################################################
# INGEST SETUP DATA
##############################################################################

ingest_photostream_app_kafka_kinesis = {
    "ingest_name": "Road Footage from Kinetica Dashcam Mobile App",
    "ingest_desc": "Road Footage from Kinetica Dashcam Mobile App",
    "ingest_mode": "CONTINUOUS",
    "ingest_type": "BYOC",                 
    "ingest_config": 
    {
        "src_uri": "kinetica/ctnr-kml-byoc-kinesis-photoapp:r7.1.0",
        "table_name": "dashcam_snapapp_inbounds",
        "env_vars":
        {
            "AWS_ACCESS_KEY_ID": "AKIAI3ODIWU3FEOTTFSA",
            "AWS_SECRET_ACCESS_KEY": "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",
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_KINESIS_PRODUCER_TOPIC": "kinetica",
        }
    }
}

ingest_photostream_byoc_mapillarry = {
    "ingest_name": "Road Footage from Mapillary",
    "ingest_desc": "Road Footage from Mapillary",
    "ingest_mode": "CONTINUOUS",
    "ingest_type": "BYOC",                 
    "ingest_config": 
    {
        "src_uri": "kinetica/ctnr-kml-byoc-sample-mapillary:r7.1.0",
        "table_name": "dashcam_mapillary_inbound",
        "env_vars":
        {
            "MAPILLARY_API_CLIENT_ID": "YVJuOGk4NFI2RmxPdWpHT3pDQ3l0Mjo5NzI4OTIyNWEwMTA1ZWFl",
            "COORDINATE_CENTER_LAT": "37.4476237",
            "COORDINATE_CENTER_LONG": "-122.1598575",
            "RADIUS": "10000",
            "CAPTURE_IMAGE_BINARY": "FALSE"
        }
    }
}



##############################################################################
# CREDENTIAL SETUP DATA
##############################################################################

credential_manifest = {
    "credential_name":"IEX Live Feed API Credentials", 
    "credential_desc":"Investors Exchange (IEX) Live Feed API Credentials", 
    "credential_type":"KAFKA",
    "credential_config":{
        "connection_str":"kafka.kinetica.com:9092",
        "topics":"roadcam",
        "keystore":"",
        "key_password":"nightingale"}
        }
        

credential_manifestx = {"credential_name":"AWS Saif Ahmed Personal",
    "credential_desc":"AWS Saif Ahmed Personal",
    "credential_type":"AWS_S3",
    "credential_config":{
        's3_bucket': 'kinetica',
        's3_path': 'kinetica/datalets',
        'aws_access_key_id': 'AKIAJX43VJUEBQMELIBA',
        'aws_secret_access_key': '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'}
        },