import cvp
from pprint import pprint


host = '192.168.10.100'
server = cvp.Cvp(host)
server.authenticate('jpatterson','P3pp3r101!')

#This is a function to find all devices within cvp

def findalldevices():

    deviceList = []


    for device in server.getDevices():

        deviceName = device.fqdn #calls the cvp api for device.fqdn

        deviceList.append(deviceName) #appens to the list each item

        dynamicList = [str(i) for i in deviceList]

    return dynamicList

for device in server.getDevices():
    pprint(device.jsonable())




dynamic = findalldevices()

def dynamic_inventory():


    pprint  ({

            'arista': {

                'hosts': dynamic,

                'vars': {

                    'ansible_connection': "local",

                    'username': 'admin',

                    'password': 'admin',

                    'transport': 'cli',

		    'use_ssl': 'true',

                }

	    }

     })

dynamic_inventory()

pprint(dir(cvp))