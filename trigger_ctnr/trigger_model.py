"""Trigger script for *continuous* feed of MV to FS Risk Model."""

__author__ = "Saif Ahmed"
__copyright__ = "Copyright 2020, KineticaDB, Inc. All rights reserved."
__credits__ = ["Saif Ahmed", "Julian Jenkins"]
__maintainer__ = "Saif Ahmed"
__email__ = "sahmed@kinetica.com"

import os
import sys
import time
import traceback
import collections
import logging
import argparse

import gpudb

logger = logging.getLogger("trigger")
logger.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER_C = logging.StreamHandler(sys.stdout)
HANDLER_C.setFormatter(FORMATTER)
logger.addHandler(HANDLER_C)


def main():

    parser = argparse.ArgumentParser(description='Trigger Script')
    parser.add_argument('--delay', type=int, choices=range(0, 30), default=5)
    parser.add_argument('--db-conn-str', help='Kinetica DB connection string, e.g.: http://187.187.187.187:9191', default=None)
    parser.add_argument('--db-conn-user', help='Kinetica DB username', default=None)
    parser.add_argument('--db-conn-pass', help='Kinetica DB password', default=None)

    parser.add_argument('--db-src-table', help='Kinetica DB source table', default="sensitivity_master")
    parser.add_argument('--db-dest-table', help='Kinetica DB destination table', default="risk_inputs")

    args = parser.parse_args()
    for arg in vars(args):
        logger.info(f"Command line argument: {arg}: {getattr(args, arg)}")

    if not args.db_conn_str:
        logger.error("Mandatory database connection string parameter not provided.")
        sys.exit(1)

    try:
        logger.debug(f"Attempting DB connection to {args.db_conn_str}")
        db = gpudb.GPUdb(args.db_conn_str)
        # TODO: also support connections w/ username+password
        if "status_info" not in db.show_system_status():
            logger.error(f"Difficulties connecting to {args.db_conn_str}")
            sys.exit(1)
        if "status" not in db.show_system_status()["status_info"]:
            logger.error(f"Difficulties connecting to {args.db_conn_str}")
            sys.exit(1)
        if  "OK" != db.show_system_status()["status_info"]["status"]:
            logger.error(f"Difficulties connecting to {args.db_conn_str}")
            sys.exit(1)

        h_data_source = gpudb.GPUdbTable(name=args.db_src_table, db=db)
        h_data_sink = gpudb.GPUdbTable(name=args.db_dest_table, db=db)

    except gpudb.gpudb.GPUdbException as e:
        print(e)
        print(traceback.format_exc())


    logger.debug(f"DB connection to {args.db_conn_str} successful, initiating trigger loop")
    while True:

        try:
            insert_queue = []
            srcitems = h_data_source.get_records()
            for s in srcitems:
                insertable = collections.OrderedDict()
                for col in [c.name for c in h_data_source.get_table_type().columns]:
                    insertable[col] = s[col]
                insert_queue.append(insertable)
            logger.info(f"Triggering insert of {len(insert_queue)} records")
            h_data_sink.insert_records(insert_queue)

            time.sleep(args.delay)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print('\nWaiting to reconnect ...')
            time.sleep(30)
            pass

if __name__ == "__main__":
    print(r"""
        ___________      .__                               _________            .__        __
        \__    ___/______|__| ____   ____   ___________   /   _____/ ___________|__|______/  |_
          |    |  \_  __ \  |/ ___\ / ___\_/ __ \_  __ \  \_____  \_/ ___\_  __ \  \____ \   __\
          |    |   |  | \/  / /_/  > /_/  >  ___/|  | \/  /        \  \___|  | \/  |  |_> >  |
          |____|   |__|  |__\___  /\___  / \___  >__|    /_______  /\___  >__|  |__|   __/|__|
                           /_____//_____/      \/                \/     \/         |__|

        """)

    main()