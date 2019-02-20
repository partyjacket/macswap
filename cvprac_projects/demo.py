
from jsonrpclib import Server
from pprint import pprint as pp


url = "http://admin:admin@192.168.10.1/command-api"
switch = Server(url)


# result_mgmt_interface = switch.runCmds(1, ['enable', {'cmd': 'show ip interface'}])[1]['interfaces']
# pp(result_mgmt_interface)


show_ip_vrf = switch.runCmds(1, ['enable', 'show ip route vrf red'])

pp(show_ip_vrf)