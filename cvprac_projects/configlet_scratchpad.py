import sys
from jsonrpclib import Server
from pprint import pprint as pp



user = 'jpatterson'
passwd = 'P3pp3r101!'
ip = '192.168.11.1'
url = "http://%s:%s@%s/command-api" % (user, passwd, ip)
switch = Server(url)


result_mgmt_interface = switch.run_Cmds(1, ['enable', {'cmd': 'show ip interface'}])[1]['interfaces']
mgmt_vlan = 'Vlan1910'
mgmt1 = 'Management1'


def get_mgmt_ip():
    if mgmt_vlan in result_mgmt_interface:
        mgmt_iface = switch.runCmds(1, ["enable", {"cmd": "show interfaces Vlan1910"}])[1]['interfaces']['Vlan1910']['interfaceAddress'][0]['primaryIp']['address']
        return mgmt_iface
    else:
        if mgmt1 in result_mgmt_interface:
            mgmt_iface = switch.runCmds(1, ["enable", {"cmd": "show interfaces management 1"}])[1]['interfaces']['Management1']['interfaceAddress'][0]['primaryIp']['address']
            return mgmt_iface

print get_mgmt_ip()


vlans_proposed = '201'
ports_proposed = ['9', ',', '1', '6', ',', '4', ',', '3', ',', '1', '2']
eth = 'Interface Ethernet'
swi_acc = 'switchport access vlan'

# get current vlan info from switch | create list of current vlans
vlans_from_switch = switch.runCmds(1, ['enable', {'cmd': 'show vlan'}])[1]['vlans']

vlans_current = [vlan for vlan in vlans_from_switch]
port_strip_ethernet_tag = []
string_ports_proposed = []
join_ports_proposed = []

for item in ports_proposed:
    string_ports_proposed.append(str(item))
string_ports_proposed.append(',')


index = 0
for item in string_ports_proposed:
    next_index = index + 1
    if next_index == len(string_ports_proposed):
        break

    elif string_ports_proposed[index].isdigit() and string_ports_proposed[next_index].isdigit():
        newdigit = string_ports_proposed[index] + string_ports_proposed[next_index]
        join_ports_proposed.append(newdigit)
        index = index + 2

    elif string_ports_proposed[index].isdigit() and string_ports_proposed[next_index] == ',':
        join_ports_proposed.append(string_ports_proposed[index])
        index += 1

    elif string_ports_proposed[index].isdigit():
        join_ports_proposed.append(string_ports_proposed[index])
        index += 1
    elif string_ports_proposed[index] == ',':
        index += 1


join_ports_proposed = [int(x) for x in join_ports_proposed]
join_ports_proposed.sort()



while vlans_proposed not in vlans_current:
    print "Vlan %s" % vlans_proposed
    if len(join_ports_proposed) == 0:
        break
    elif len(join_ports_proposed) >= 1:
        for port_proposed in join_ports_proposed:
            print "%s %s\n\t%s %s" % (eth, port_proposed, swi_acc, vlans_proposed)
        break


else:
    vlan_port_result = switch.runCmds(1, ['enable', {'cmd': 'show vlan %s configured-ports' % vlans_proposed}])[1]['vlans']['%s' % vlans_proposed]['interfaces']
    if len(vlan_port_result) > 1:
        ports_current = [port for port in vlan_port_result]
        vxlan = 'Vxlan1'
        if vxlan in ports_current:
            ports_current.remove(vxlan)
        for port in ports_current:
            port_strip_ethernet_tag.append(port[8:])
        for port_proposed in join_ports_proposed:
            if port_proposed not in port_strip_ethernet_tag:
                print "%s %s\n\t%s %s" % (eth, port_proposed, swi_acc, vlans_proposed)






