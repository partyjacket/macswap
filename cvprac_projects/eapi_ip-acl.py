from jsonrpclib import Server
from arista_nest_helper import myhelper
from pprint import pprint as pp
import cvprac




user = 'jpatterson'
passwd = 'P3pp3r101!'
ip = '192.168.10.1'
# url = "http://%s:%s@%s/command-api" % (user, passwd, ip)
ss = Server("http://%s:%s@%s/command-api" % (user, passwd, ip))


show_version = ss.runCmds(1, [{'cmd': 'show version'}])[0]['version']

print "The code on this box is %s." % show_version

pp(show_version)

# myhelper(show_version)

def acl(user, passwd, ip):
    url = 'http://%s:%s@%s/command-api' % (user, passwd, ip)
    ss = Server(url)
    ss.runCmds(1, [
        'enable',
        'configure terminal',
        'ip access-list jason',
        '10 permit ip 192.168.0.0/24 any',
        '20 permit ip 172.16.0.0/12 any',
        '30 permit ip 0.0.0.0/0 any',
        '40 permit ip any any'
        ]
    )


def no_acl(user, passwd, ip):
    url='http://%s:%s@%s/command-api' % (user, passwd, ip)
    ss = Server(url)
    ss.runCmds(1, ['enable', 'configure terminal', 'no ip access-list jason'])


no_acl(user, passwd, ip)




