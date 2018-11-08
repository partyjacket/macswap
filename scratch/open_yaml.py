#!/usr/bin/python

import yaml
import sys
from pprint import pprint as pp
import time

with open('../ansible_files/hosts') as f:
	read_f = f.read()
	print read_f


with open('../ansible_files/raw.yml') as f:
	load_f = yaml.load(f)
	pp(load_f)

with open('newfile', 'a') as temp:
	temp.write('\nThis is a new entry4')

with open('newfile') as f:
	print f.read()

with open('newfile') as f:
	test = f.readlines()
	time.sleep(5)
	print len(test)
	print type(test)

sys.exit('jo mamas script just made an exit, it is finished')

