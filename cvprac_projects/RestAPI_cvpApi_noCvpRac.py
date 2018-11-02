import requests
import json
from pprint import pprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # This will disable invalid cert warnings





cvp_user = 'jpatterson'
cvp_pass = 'P3pp3r101!'
cvp_host = '192.168.10.100'

auth_data = json.dumps({'userId': cvp_user, 'password': cvp_pass})
auth_url = auth_url = "https://%s/cvpservice/login/authenticate.do" % cvp_host
auth_response = requests.post(auth_url, data=auth_data, verify=False)
assert auth_response.ok
cookies = auth_response.cookies

# print auth_response.json()

task_params = {'startIndex': '0', 'endIndex': '0'}
task_url = 'https://%s/cvpservice/snapshot/getSnapshots.do?' % cvp_host
task_response = requests.get(task_url, cookies=cookies, params=task_params, verify=False)

pprint(task_response.json())
