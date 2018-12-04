from __future__ import print_function

import argparse
import sys

import grpc
import grpc.framework.interfaces.face

import pyopenconfig.openconfig_pb2
import pyopenconfig.resources
from pprint import pprint as pp

import json


def get(stub, path_str, metadata):
    """Get and echo the response"""
    response = stub.Get(pyopenconfig.resources.make_get_request(path_str),
                        metadata=metadata)
    return response


def subscribe(stub, path_str, metadata):
    """Subscribe and echo the stream"""
    subscribe_request = pyopenconfig.resources.make_subscribe_request(path_str=path_str)
    i = 0
    try:
        for response in stub.Subscribe(subscribe_request, metadata=metadata):
            print(response)
            i += 1
    except grpc.framework.interfaces.face.face.AbortionError, error:  # pylint: disable=catching-non-exception
        if error.code == grpc.StatusCode.OUT_OF_RANGE and error.details == 'EOF':
            # https://github.com/grpc/grpc/issues/7192
            sys.stderr.write('EOF after %d updates\n' % i)
        else:
            raise


metadata = [("username", 'admin'), ("password", 'admin')]

host = grpc.insecure_channel('192.168.10.1:6042')
stub = pyopenconfig.openconfig_pb2.OpenConfigStub(host)
path = '/Sysdb/interface/counter/eth/'




test2 = get(stub, path, metadata)

munch = open('new.txt', 'w')
munch.write(test2)
munch.close()




