from pprint import pprint
from cvprac.cvp_client import CvpClient
from cvprac.cvp_api import CvpApi
import urllib3

import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # This will disable invalid cert warnings

client = CvpClient()

client.connect(['cvp.lab.local'], 'jpatterson', 'P3pp3r101!')


cvp = CvpApi(client)
# test = cvp.get_cvp_info()
# print test
#
# gettask = cvp.get_tasks()
# pprint(gettask)

'''Get inventory of CVP, then strip out FQDN of hostname and present just hostname:'''
# host_list = []
# def hostname(filter=''):
#     inventory = cvp.get_inventory(query=filter)
#     full_fqdn = 'lab.local'
#     for value in inventory:
#         if full_fqdn in value['fqdn']:
#             fqdn_strip = value['fqdn'][0:-10]
#             host_list.append(fqdn_strip)
#     return host_list
#
# hostname()
#
# for name in host_list:
#     print name
#
# def finditem(filter=''):
#     inventory = cvp.get_inventory(query=filter)
#     pprint(inventory[0]['fqdn'])
#
#
# finditem('192.168.10.1')



# def ip_to_host():
#     ip_addr = raw_input('Please enter the IP address of the host: ')
#     inventory = cvp.get_inventory()
#     for key in inventory:
#         if ip_addr in key['ipAddress']:
#             print "The hostname with the IP address of %s is: " % ip_addr, key['fqdn']
#
# ip_to_host()

'''Must save funtion output (dictionary) into variable before typical .items, keys, value methods can be invoked'''
mydict = cvp.get_containers()
for item in mydict['data']:
    print item['name'], item['key']

'''adding a device to CVP and saving the state once done:'''
# add_dev = cvp.add_device_to_inventory('192.168.11.12', 'SL-DC', 'container_17_609729386866')
# time.sleep(15) #sleep between adding device, and then saving the addition:
# save_state = cvp.save_inventory()
# # print save_state





# def add_device(devip):
#     cvp.add_device_to_inventory(devip, 'SL-DC')



# configlet_name = 'VLANS'
# configlet_content = 'vlan 100\n   name DEMO\nend'
# result = client.api.add_configlet(configlet_name, configlet_content)
# pprint(result)
#
# configlet_info = client.api.get_configlet_by_name(configlet_name)
# pprint(configlet_info)


