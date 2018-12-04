#!/usr/bin/python

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-a', action="store_true", default=False, dest='bool')
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)

results = parser.parse_args(['-a', '-b', 'val', '-c', '20'])


if results.bool:
    print 'its true yall'
if results.b:
    print 'This is the result of %s' % results.b
if results.c:
    print 'This is the result of %d' % results.c

print results
#
# device_list = ['10.10.10.11', '10.10.10.12', '10.10.10.13']
# new_devices = ['10.10.10.14', '10.10.10.15', '10.10.10.16']
# newdevs = device_list.__add__(new_devices)

# print newdevs.__contains__('10.10.10.14')
#
# newdevs.remove('10.10.10.11')



# device_list.extend(new_devices)
#
# new_device_ip = '10.10.10.17'
# device_list.append(new_device_ip)

# print '\n'.join(dir(argparse.ArgumentParser))

