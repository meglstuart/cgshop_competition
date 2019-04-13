from Hashable2dGeometry import Point, Segment
import numpy as np
import collections

class QueueElem:
    def __init__(self, pt):
        self.pt = pt
        self.segs = set()

    def __str__(self):
        return str(self.pt)

    def __gt__(self,other):
        return self.pt > other.pt


def readdata(filename):
    list_data = list()
    with open(filename, 'r') as f:
        lines = f.readlines()

    for l in lines:
        l.strip()
        if (len(l) != 0 and l[0] != '#'):
            [i, x, y] = l.split()
            list_data.append(Point(int(x),int(y)))
    return list_data


inst = 10
instance_file = "/Users/meg/repos/cgshop_competition/challenge_instances/data/images/euro-night-" + str(inst).zfill(7) + ".instance"
vertices = readdata(instance_file)

Q = dict([(v,set()) for v in vertices])
Q = collections.OrderedDict(sorted(Q.items()))


all_possible_edges = set()
for pt in vertices:
    for ptB in vertices:
        if ptB > pt:
            all_possible_edges.add(Segment(pt, ptB))
            Q[pt].add(Segment(pt,ptB))

for q,S in Q.items():
    print(q)
    for s in S:
        print(s)

count = 0
for seg1 in all_possible_edges:
    for seg2 in all_possible_edges:
        if seg1.A != seg2.A and seg1.B != seg2.B and seg1.A != seg2.B and seg1.B != seg2.A:
            if seg1.intersects(seg2):
                # print(str(seg1)+" intersects with "+str(seg2))
                count += 1

print("there were " + str(count) + " segment intersections")
