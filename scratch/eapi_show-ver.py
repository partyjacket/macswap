import pyeapi

br = pyeapi.connect(host='192.168.10.1', username='admin', password='admin')

print br.execute('show version')





