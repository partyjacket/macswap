import os
import time



def redirect_to_file():
    while True:
        time.sleep(5)
        os.system('ping ' + '-c 2 ' + '192.168.11.11 ' + '>> ' + 'pinglog.txt')


if __name__ == '__main__':
    redirect_to_file()