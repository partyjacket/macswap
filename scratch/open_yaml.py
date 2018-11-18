#!/usr/bin/python

import yaml
import sys
from pprint import pprint as pp
import time
import json

x = ['item1', 'item2', 2, 3, {'mydict': 'myitem'}]
with open('../ansible_files/hosts') as f:
	read_f = f.read()
	print read_f


with open('../ansible_files/raw.yml') as f:
	load_f = yaml.load(f)
	pp(load_f)

# with open('newfile', 'a') as temp:
# 	for num in range(5):
# 		nutz = str(num)
# 		temp.write(nutz)


with open('newfile', 'w') as n:
	for item in x:
		json.dump(item, n)


with open('newfile') as f:
	test = f.readlines()
	time.sleep(5)
	print len(test)
	print type(test)

# sys.exit('jo mamas script just made an exit, it is finished')

list1 = ['1', '2,', '3']

val1, val2, val3 = list1
print val2

