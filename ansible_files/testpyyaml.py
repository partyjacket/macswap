#!/usr/bin

import yaml
from pprint import pprint as pp

with open('shver.yml') as f:
    result = yaml.load(f)
    pp(result)


with open('raw.yml') as g:
    result = yaml.load(g)

