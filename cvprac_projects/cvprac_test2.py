from pprint import pprint
from cvprac.cvp_client import CvpClient
from cvprac.cvp_api import CvpApi
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # This will disable invalid cert warnings


client = CvpClient()
api = CvpApi(client)


client.connect(['cvp.lab.local'], 'jpatterson', 'P3pp3r101!')


result = client.get('/cvpInfo/getCvpInfo.do')

newresult = client.get('https://cvp.lab.local/cvpservice/image/getImages.do?startIndex=0&endIndex=0')

print newresult


# test1 = clnt.get('/cvpservice/snapshot/getSnapshots.do?startIndex=0&endIndex=0')

print result
