#!/usr/bin/env python3
"""Monitor key aspects of the market risk FS demo."""

import requests
import datetime
import gpudb
import time
import argparse

# Defaults
timeout = 30
host_default = '172.31.32.22'    # Kinetica production cluster

parser = argparse.ArgumentParser()
parser.add_argument('--host', default=host_default, help='Hostname')
parser.add_argument('--aaw-port', default=9187, help='Workbench port')
parser.add_argument('--db-port', default=9191, help='Database port')
parser.add_argument('--interval', default=300, help='Polling interval')
args = parser.parse_args()

ip = args.host
db_port = args.db_port
aaw_api_port = args.aaw_port
poll_interval = int(args.interval)

# Get DB handle
db = gpudb.GPUdb(f'http://{ip}:{db_port}')

# Init counts
n_risk_in_last = 0
n_risk_out_last = 0
n_activity_last = 0

print(f'Starting Financial Services Demo monitor')
print(f'Polling every {poll_interval} seconds ({round(poll_interval/60, 2)} minutes)')
print(f'Database:\t{ip}:{db_port}')
print(f'Workbench:\t{ip}:{aaw_api_port}')

while True:

    try:
        # Start loop
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print('========')
        print('Timestamp: ', end='\t')
        print(f'{dt}')

        # Test DB API
        #  print('Testing DB API')
        #  port = 9191
        #  url = f'http://{ip}:{port}'
        #  r = requests.get(url, timeout=timeout)
        #  if r.status_code != 200:
        #      dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        #      print(f'{dt}  Database API unresponsive')

        # Test AAW API
        print('API status: ', end='\t')
        port = aaw_api_port
        url = f'http://{ip}:{port}'
        t0 = time.time()
        r = requests.get(url, timeout=timeout)
        resp_time = time.time() - t0
        if r.status_code != 200:
            print('\x1b[1;37;41m' + 'UNRESPONSIVE' + '\x1b[0m')
        else:
            print(f'{round(resp_time, 4)} sec response')
        time.sleep(1)

        # Test AAW UI
        #  print('Testing AAW UI')
        #  port = 8070
        #  url = f'http://{ip}:{port}'
        #  r = requests.get(url, timeout=timeout)
        #  if r.status_code != 200:
        #      dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        #      print(f'{dt}  Workbench UI unresponsive')

        # Test GAdmin
        #  print('Testing GAdmin')
        #  port = 8080
        #  url = f'http://{ip}:{port}'
        #  r = requests.get(url, timeout=timeout)
        #  if r.status_code != 200:
        #      dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        #      print(f'{dt}  Database GAdmin unresponsive')

        # Test Reveal
        #  print('Testing Reveal')
        #  port = 8088
        #  url = f'http://{ip}:{port}/caravel/dashboard/2/'
        #  r = requests.get(url, timeout=timeout)
        #  if r.status_code != 200:
        #      dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        #      print(f'{dt}  Reveal dashboard unresponsive')

        # Check increase in iex activity (capture stream running)
        print('Stream: ', end='\t')
        n_activity = gpudb.GPUdbTable(name='iex_stream',
                                      db=db).count
        if not n_activity > n_activity_last:
            print('\x1b[1;37;41m' + 'NOT UPDATING' + '\x1b[0m')
        else:
            print('Running')
        n_activity_last = n_activity
        time.sleep(1)

        # Check increase in risk_inputs (trigger running)
        print('Model input: ', end='\t')
        n_risk_in = gpudb.GPUdbTable(name='risk_inputs',
                                     db=db).count
        if not n_risk_in > n_risk_in_last:
            print('\x1b[1;37;41m' + 'NOT UPDATING' + '\x1b[0m')
        else:
            print('Running')
        n_risk_in_last = n_risk_in
        time.sleep(1)

        #  Check increase in risk_outputs (model running)
        print('Model output: ', end='\t')
        n_risk_out = gpudb.GPUdbTable(name='risk_outputs',
                                      db=db).count
        if not n_risk_out > n_risk_out_last:
            print('\x1b[1;37;41m' + 'NOT UPDATING' + '\x1b[0m')
        else:
            print('Running')
        n_risk_out_last = n_risk_out

        if poll_interval >= 60:
            print(f'Waiting {round(poll_interval/60, 1)} min')
        else:
            print(f'Waiting {poll_interval} sec')
        time.sleep(poll_interval)

    except Exception as e:
        print(e)
