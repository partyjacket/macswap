import os, sys

# os.system("ping -c 1 '192.168.10.1'")
# print os


def test():
    print 'this is the def', os.getcwd()



if __name__ == "__main__":
    test()
else:
    print "nutz"

foo = 100


def hello():
    print("i am from my_module.py")


if __name__ == "__main__":
    print("Executing as main program")
    print("Value of __name__ is: ", __name__)
    hello()
else:
    print "this funct is being called from a remote module"
    print("Value of __name__ is: ", __name__)