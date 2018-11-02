#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader("/media/sf_vboxshare/jinja"))
#NV = Environment(loader=FileSystemLoader("/Users/jpatterson/Documents/#Arista/vboxshare/jinja"))

template1 = ENV.get_template('template.j2')

interface_dict = {"name": "Ethernet1", "description": "Server Port", "vlan": 10, "uplink": False}

print template1.render(interface=interface_dict)



