from jsonrpclib import Server
from pprint import pprint as pp
import os


ips = ['192.168.10.1', '192.168.11.5', '192.168.11.11', '192.168.11.12', '192.168.11.21', '192.168.11.22', '192.168.11.101', '192.168.11.102']
user = 'jpatterson'
passwd = 'P3pp3r101!'

def urls(ip):
    url = 'http://%s:%s@%s/command-api' % (user, passwd, ip)
    return url


def ta_shut():
    for ip in ips:
        url = urls(ip)
        ss = Server(url)
        ss.runCmds(1, ['enable', 'configure terminal', 'daemon TerminAttr', 'no shutdown'])
        pp(ss.runCmds(1, ['enable', 'show daemon TerminAttr']))



def ta_shut5():
    ip = '192.168.11.5'
    url = 'http://%s:%s@%s/command-api' % (user, passwd, ip)
    ss = Server(url)
    ss.runCmds(1, ['enable', 'configure terminal', 'daemon TerminAttr', 'shutdown'])
    pp(ss.runCmds(1, ['enable', 'show daemon TerminAttr']))

ta_shut()





# os.system('ping ' + '-c 2 ' + '192.168.11.1')

