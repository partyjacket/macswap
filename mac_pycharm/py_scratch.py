#!/usr/bin/python

import pyeapi
import yaml
from pprint import pprint as pp

veos1 = pyeapi.connect_to('veos1')

pp(veos1.enable('show version'))

veos1.config('hostname VEOS1')


shrun = veos1.enable('show running-config')
pp(shrun)

print "\n\n\nnow I'm going to the next section \n\n\n"

output = shrun[0]['result']['cmds']['interface Management1']['cmds']

test = output.keys()

test2 = str(test)

test3 = test2[13:31]

mgmt_statement = "The IP ADDR of MGMT1 is:"
print mgmt_statement + test3

for num in range(1,194):
    if str(num) in test3:
        print "yes" + str(num)
else:
    print "no" + str(num)

test4 = str(output)

print type(test4)

print test4

newdict = {'mykey':'myvalue'}

print test

whatComesOutYourBumBum = "poop"
for letter in "skylar":
    print whatComesOutYourBumBum

message = "Sky really has to " + whatComesOutYourBumBum
print message

brookesString = "daddy la daddy la booty boots"

print brookesString + " really has to " + whatComesOutYourBumBum


