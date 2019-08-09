from jsonrpclib import Server
from pprint import pprint as pp

# user = 'jpatterson'
# passwd = 'P3pp3r101!'
# ip = '192.168.10.1'
# url = 'http://%s:%s@%s/command-api' % (user, passwd, ip)
#
# switch = Server(url)
#
#
# def command():
#     run_command = switch.runCmds(1, ['enable', {'cmd': 'configure'}, {'cmd': 'interface ethernet 1'}, {'cmd': 'no lldp transmit'}])
#     return
#
# print show_version
# from funny import test
#
# ip = '192.168.10.1'
# user = 'jpatterson'
# passwd = 'P3pp3r101!'
# url = 'http://%s:%s@%s/command-api' % (user, passwd, ip)
# switch = Server(url)
# result = switch.runCmds(1, ['enable', 'show lldp neighbors'])[1]['lldpNeighbors'][:]



def lldp_neighbors(mac):
        ip = '192.168.10.1'
        user = 'admin'
        passwd = 'admin'
        url = 'http://%s:%s@%s/command-api' % (user, passwd, ip)
        switch = Server(url)
        result = switch.runCmds(1, ['enable', 'show lldp neighbors'])[1]['lldpNeighbors'][:]
        for value in result:
            neighbor_value = value['neighborDevice']
            print value['neighborDevice']
            if mac in neighbor_value:
                return ("Yes, I've found the damn mac!")

#         extract(result, mac)
#
#
#
# def extract(results, mac):
#     for key, value in results.iteritems():
#         if mac in value:
#             print 'holy shit'

br = lldp_neighbors('f8b1.56b5.b6a4')

pp(br)

# helper((br))


string = 'this is, my, string, did it , split, on the comma?'

newstring = string.split()

print newstring













