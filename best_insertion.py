import numpy as np

def readdata(filename):
    list_data = list()
    with open(filename, 'r') as f:
        lines = f.readlines()

    for l in lines:
        l.strip()
        if (len(l) != 0 and l[0] != '#'):
            [i, x, y] = l.split()
            list_data.append([int(x),int(y)])

    data = np.asarray(list_data)
    return data

print(readdata("/Users/meg/repos/cgshop_competition/challenge_instances/data/images/euro-night-0000010.instance"))
