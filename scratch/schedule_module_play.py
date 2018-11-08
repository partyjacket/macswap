import yaml
import sys
from pprint import pprint as pp
import time
import schedule





#
# def print_something(something = 'nutz'):
#     n = 0
#     while n < 5:
#         print 'I need to print something', something
#         n += 1
#     return n
#
#
#
# schedule.every(2).seconds.do(print_something, something = 'this is something')
#
#
#
# def main():
#     n = int()
#     print n
#     while n < 4:
#         schedule.run_pending()
#
#
# if __name__ == "__main__":
#     main()
# else:
#     print('this is not my file')

def f1():
    print("Moe") #8

def f2():
    f4() #2
    print("Meeny") #5

def f3():
    f2() #1
    print("Miny") #6
    f1() #7

def f4():
    print("Eeny") #3

f3()

