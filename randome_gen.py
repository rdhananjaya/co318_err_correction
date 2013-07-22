__author__ = 'Roshan'

MAXINT = 0x7fffffff

seed = 100

def URandome(max):
    global seed
    seed = (3141592653 * seed + 2718281829) & MAXINT
    return seed/MAXINT*max
#
# rand = URandome(1000)

err_ratio = 0.1
max_num = 1000

count = 0
for i in range(1000000):
    uand = URandome(max_num)
    if uand < 1000*err_ratio:
        count += 1


print(count/max_num)


