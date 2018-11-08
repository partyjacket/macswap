#!/usr/bin/python

import yaml
import sys
from pprint import pprint as pp

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
	print len(test)
	print type(test)

# sys.exit('jo mamas script just made an exit, it is finished')

list1 = ['1', '2,', '3']

val1, val2, val3 = list1
print val2

