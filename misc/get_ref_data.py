#!/usr/bin/env python3

import sys
import json
import random
import time
import datetime
import pprint
import traceback
import logging
import copy

from iexfinance.iexdata import get_tops
from iexfinance.stocks import Stock

SECURITIES_UNIVERSE = [line.rstrip('\n') for line in open("sec_universe.txt")]

# Build local cache of reference data
def cache_ref_data():
    ref_data = {}
    for tckr in SECURITIES_UNIVERSE:
        print(f"Handling ticker {tckr}")
        try:
            price = Stock(tckr)
            ref_data[tckr]=price.get_company()
        except Exception as e:
            print(e)
    with open('ref_data.json', 'w') as outfile:
        json.dump(ref_data, outfile)


# Build local cache of price data
def cache_hist_px():
    hist_prices = {}
    for tckr in SECURITIES_UNIVERSE:
        print(f"Handling ticker {tckr}")
        try:
            price = Stock(tckr)
            hist_prices[tckr]={}
            hist_prices[tckr]["get_previous_day_prices"]=price.get_previous_day_prices()
            hist_prices[tckr]["get_quote"]=price.get_quote()
        except Exception as e:
            print(e)    
    with open('price_data.json', 'w') as outfile:
        json.dump(hist_prices, outfile)

def get_simple_px():
    import csv
    csv_columns = ['ticker','px']
    with open('price_data.json', 'r') as infile:
        hist_prices = json.load(infile)
    write_q=[]
    for tckr in hist_prices:
        if hist_prices[tckr]:
            if "get_previous_day_prices" in hist_prices[tckr]:
                if "close" in hist_prices[tckr]["get_previous_day_prices"]:
                    write_q.append({
                        "ticker": tckr, 
                        "px": hist_prices[tckr]["get_previous_day_prices"]["close"]
                        })

    try:
        with open("ticker_px.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in write_q:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def main():
    #cache_ref_data()
    #cache_hist_px()
    get_simple_px()

if __name__ == "__main__":
    main()