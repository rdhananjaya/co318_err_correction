__author__ = 'Roshan'

import subprocess
import time

if __name__ == '__main__':
    for error_rate in range(6):
        for window_size in range(1, 6):
            for nothing in range(10): # this loop to get an average value
                arg_recv = "python Receiver.py {} {}".format(error_rate, window_size )
                print("Opening ")
                p1 = subprocess.Popen(arg_recv)
                print("Opened")
                # p1.wait(1)
                # time.sleep(1)

                arg_main = "python main.py {} {}".format(error_rate, window_size)
                print("Opening")
                p2  = subprocess.Popen(arg_main)
                print("Opened")
                p2.wait(3)
                p1.wait(3)

                # time.sleep(1)



