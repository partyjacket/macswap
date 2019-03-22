
dcSwitchDict = {'spines': ['s1', 's2'], 'leafs': {'vtep10': ['leaf11', 'leaf12'], 'vtep20': ['vtep21', 'vtep22']}}




def mygen(x):
    y = 0
    base = '192.168.10.'
    while y < x:
        yield base + str(y)
        y += 1


for i in mygen(10):
    print(i)


