import cvp
from pprint import pprint as pp
from arista_nest_helper import myhelper


host = '192.168.10.100'
server = cvp.Cvp(host)
server.authenticate('jpatterson', 'P3pp3r101!')

#This is a function to find all devices within cvp

# def findalldevices():
#
#     deviceList = []
#
#
#     for device in server.getDevices():
#
#         deviceName = device.fqdn #calls the cvp api for device.fqdn
#
#         deviceList.append(deviceName) #appens to the list each item
#
#         dynamicList = [str(i) for i in deviceList]
#
#     return dynamicList

# for device in server.getDevices():
#     pprint(device.jsonable())

# for device in server.getConfiglets():
dev_configlets = [devconfig for devconfig in server.getConfiglets()]
devlist = dev_configlets[0].jsonable()

# pp(devlist)
myhelper(devlist['formList'])


print devlist['formList']

for item in devlist['formList']:
    print item['fieldLabel']

print dev_configlets  

fqnd_list = [device.fqdn for device in server.getDevices()]
print fqnd_list


# dynamic = findalldevices()
#
# def dynamic_inventory():
#
#
#     pprint  ({
#
#             'arista': {
#
#                 'hosts': dynamic,
#
#                 'vars': {
#
#                     'ansible_connection': "local",
#
#                     'username': 'admin',
#
#                     'password': 'admin',
#
#                     'transport': 'cli',
#
# 		    'use_ssl': 'true',
#
#                 }
#
# 	    }
#
#      })
#
# dynamic_inventory()
#
# pprint(dir(cvp))