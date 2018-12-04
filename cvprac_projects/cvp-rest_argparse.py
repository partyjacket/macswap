#!/usr/bin/python

import requests
from pprint import pprint as pp
import json
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # This will disable invalid cert warnings
import argparse

parser = argparse.ArgumentParser()

cvp_user = ''
cvp_pass = ''
cvp_host = ''

parser.add_argument('-u', '--user', action='store', dest='cvp_user', default='jpatterson')
parser.add_argument('-p', '--password', action='store', dest='cvp_pass', default='P3pp3r101!')
parser.add_argument('-n', '--node', action='store', dest='cvp_host', default='192.168.10.100')

result = parser.parse_args()


user = json.dumps({'userId': result.cvp_user})
passwd = json.dumps({'password': result.cvp_pass})

auth_data = json.dumps({'userId': result.cvp_user, 'password': result.cvp_pass})
auth_url = auth_url = "https://%s/cvpservice/login/authenticate.do" % result.cvp_host
auth_response = requests.post(auth_url, data=auth_data, verify=False)
assert auth_response.ok
cookies = auth_response.cookies

new_reqest = requests.get('https://%s/cvpservice/configlet/getConfiglets.do?startIndex=0&endIndex=0' % result.cvp_host, cookies=cookies, verify=False)
pp(new_reqest.json())


