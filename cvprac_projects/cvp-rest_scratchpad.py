from mylib import cvp
from mylib import cvpServices
from pprint import pprint as pp
from arista_nest_helper import myhelper
import json
import requests

ip = '192.168.10.100'
connect_cvp = cvpServices.CvpService(host=ip, ssl=True, port=443, )
connect_cvp.authenticate('jpatterson', 'P3pp3r101!')
cvp_host = '192.168.10.100'

# #######################################################################################
#
# images = connect_cvp.getImagesInfo()
# imagelist = [image for image in images]
# for item in imagelist:
#     for key, value in item.iteritems():
#         print 'key: %-25s value: %s' % (key, value)
#
# for index, item in enumerate(imagelist):
#     print index
# for item in images:
#     for key, value in item.items():
#         print 'key: %-25s value: %s' % (key, value)
#
# ########################################################################################

task_url = 'https://%s/cvpservice/configlet/getConfiglets.do?startIndex=0&endIndex=0' % cvp_host
task_response = connect_cvp.doRequest(requests.get, task_url)

dope = task_response['data'][0]
mydict = dict(dope)
for key, value in mydict.iteritems():
    print key, value


container = connect_cvp.getInventory()
pp(container)

container_list_url = 'https://cvp.lab.local/cvpservice/inventory/containers'
container_list = connect_cvp.doRequest(requests.get, container_list_url)
pp(container_list)

getid = connect_cvp.getContainerInfoByKey('container_76_1207992792122')
print getid

devid = connect_cvp.getNetElementById('0c:89:f7:02:6a:d4')
pp(devid)







