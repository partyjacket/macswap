from pprint import pprint
from cvprac.cvp_client import CvpClient
from cvprac.cvp_api import CvpApi
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # This will disable invalid cert warnings


clnt = CvpClient()

clnt.connect(['cvp.lab.local'], 'jpatterson', 'P3pp3r101!')

result = clnt.get('/cvpInfo/getCvpInfo.do')

test1 = clnt.get('/cvpservice/snapshot/getSnapshots.do?startIndex=0&endIndex=0')


pprint(result)