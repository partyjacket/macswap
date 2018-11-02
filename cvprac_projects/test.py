import pyeapi
import yaml
from pprint import pprint as pp

br1 = pyeapi.connect_to('test')


pp(br1.enable('show version'))

# br1.config('hostname ballz')
#
#
# shrun = br1.enable('show running-config')
#
# pp(br1.enable('show version'))
#
# br1.config('hostname ballz2')
#
#
# shrun = br1.enable('show running-config')
# pp(shrun)
#
# print "\n\n\nnow I'm going to the next section \n\n\n"
#
# output = shrun[0]['result']['cmds']['interface Management1']['cmds']
#
# test = output.keys()
#
# print test

