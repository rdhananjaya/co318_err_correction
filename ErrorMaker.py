from random import random

def prob_err(err_rate, length):
    q = map( lambda x: x < err_rate, ( random()*100 for i in range(length)))
    return q


def add_err(counter, err_rate):
    """ add_err return the counter same as the input when it decides to make it error free and return 0 when it decides
     to make it errored.
    """
    #return counter # this will make all the packets error free

    r = random()*100
    if r < err_rate:
        counter = 0
    return counter