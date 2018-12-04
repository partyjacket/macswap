#!/usr/bin/python

import pyeapi
import yaml
from pprint import pprint as pp
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', action='store', dest='uri', help='type "-f", then space,'
                                                           ' then path/to/config_file', default='~/.eapi.conf')

results = parser.parse_args()

def load_config(uri):
    pyeapi.load_config(uri)
    br1 = pyeapi.connect_to('test')
    pp(br1.enable('show version'))


if results.uri:
    load_config(results.uri)






