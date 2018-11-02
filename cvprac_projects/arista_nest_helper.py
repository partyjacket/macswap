import sys
from jsonrpclib import Server
from pprint import pprint as pp


def myhelper(result_command):
    print '\nThe type of nested object is: ' + str(type(result_command)) + '.'
    print 'There are %s nested objects at this level.' % str(len(result_command))


