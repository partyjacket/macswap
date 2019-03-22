#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader

#ENV = Environment(loader=FileSystemLoader("/media/sf_vboxshare/jinja_files"))
ENV = Environment(loader=FileSystemLoader("/Users/jpatterson/Documents/vboxshare/macswap/automation_book/basic_python-jinja/jinja_files/"))

template1 = ENV.get_template('template3.j2')


class NetworkInterface(object):
    def __init__(self, name, description, vlan, uplink=False):
        self.name = name
        self.description = description
        self.vlan = vlan
        self.uplink = uplink


interface_obj = NetworkInterface("Ethernet50", "This is my interface", "100")

print(template1.render(interface=interface_obj))



