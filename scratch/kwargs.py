# from schedule_module_play import print_something
#
#
# print_something("I'm calling this file remote - so it's not called '__main__' !!!")



mydict = dict()
def myiteritems(**kwargs):
    for a, b in kwargs.iteritems():
        mydict[a] = b



myiteritems(jason = 3)

print mydict

mydict['test'] = 'nutz'

print mydict














