import os
import time



def redirect_to_file():
    x = 0
    while True:
        if x == 3:
            return False
        x += 1
        time.sleep(2)
        os.system('ping ' + '-c 2 ' + '192.168.10.1 ' + '>> ' + 'pinglog.txt')


if __name__ == '__main__':
    redirect_to_file()