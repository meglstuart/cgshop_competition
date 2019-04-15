#!/usr/bin/env python3

from Hashable2dGeometry import Point, Segment, Orientation
import numpy as np
# import collections
from sortedcontainers import SortedDict
from blist import blist
# https://pypi.org/project/blist/
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

class QueueElem:
    def __init__(self, pt):
        self.pt = pt
        self.segs = set()

    def __str__(self):
        return str(self.pt)

    def __gt__(self,other):
        return self.pt > other.pt

    def __eq__(self, other):
        return self.pt == other.pt

    def __hash__(self):
        return hash(hash(pt))


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

def binSearchT(T, l, r, p):
    """
    Returns leftmost segment containing p
    """
    if r>=l:
        mid = l + (r - l)//2
        o = Orientation(T[mid].A, T[mid].B, p)
        if (o == 0 or o==1) and (mid == 0 or Orientation(T[mid-1].A, T[mid-1].B, p)==2):
            return mid
        elif o == 2:
            return binSearchT(T,mid+1, r,p)
        else:
            return binSearchT(T,l, mid-1,p)

    return -1


def searchInT(T, p):
    """
    Given a blist of segments T, and a point p, returns the set, L, of segments in T whose lower endpoints are p, and the set, C, of segments in T who contain p in their interior, and removes L union C from T. These segments are adjacent in T. It also returns i, the index of the first removed segment.
    """
    L = set()
    C = set()
    firstSeg = -1
    # for seg in T:
    #     print(seg)

    # for j in range(len(T)):
    #     if T[j].onSegment(p):
    #         # print("point " + str(p) + " is on segment " + str(T[j]))
    #         firstSeg = j
    #         break
    # print(firstSeg)
    firstSeg = binSearchT(T,0,len(T)-1,p)
    # print(firstSeg)

    if firstSeg != -1:
        while firstSeg < len(T) and T[firstSeg].onSegment(p):
            if T[firstSeg].B == p:
                L.add(T.pop(firstSeg))
            # elif T[firstSeg].A != p:
            else:
                # print("in the interior")
                C.add(T.pop(firstSeg))
    return L, C, firstSeg

def findNewEvent(sl,sr,p,Q):
    doesInt, intPt = sl.intersectionPoint(sr)
    if doesInt:
        if intPt > p:
            Q.setdefault(intPt,set())
                # Q.move_to_end(intPt, last=False)
        # print(str(sl) + "intersects with " + str(sr) + " at point "+ str(intPt))
        # print(sl.onSegment(intPt))
        # print(sr.onSegment(intPt))

def handleEventPoint(p,U,T,Q):
    """
    p is the event point, U is the set of segments with upper endpoint U, and T is the status structure blist, Q is the event queue
    """
    global intCount
    # print("before delete")
    # for t in T:
    #     print(t)
    L, C, ind = searchInT(T, p)
    if len(C) != 0:
        # print(str(p) + " is in the interior of these segments:")
        # for c in C:
        #     print(c)
        # print("and and an endpoint of these segments")
        # for x in L.union(U):
        #     print(x)
        intCount+=1
    toInsert = list(U.union(C))
    toInsert.sort()
    # print("before insert")
    # for t in T:
    #     print(t)

    if(len(T) == 0):
        ind = 0
    # else:
    #     if ind == -1:
    #         for i in range(len(T)):
    #             if Orientation(T[i].A,T[i].B,p) != 1:
    #                 ind = i
    #                 break
    for seg in toInsert:
        T.insert(ind,seg)
    # print("after insert")
    # for t in T:
    #     print(t)
    if len(toInsert) == 0:
        if(ind-1 >=0):
            sl = T[ind-1]
            sr = T[ind]
            findNewEvent(sl,sr,p,Q)
    else:
        if ind-1 >=0:
            s_prime = toInsert[-1]
            sl = T[ind-1]
            # print("checking intersection of "+str(sl)+" and "+str(s_prime))
            findNewEvent(sl,s_prime,p,Q)
        if ind+len(toInsert)<len(T):
            s_2prime = toInsert[0]
            sr = T[ind+len(toInsert)]
            # print("checking intersection of "+str(s_2prime)+" and "+str(sr))
            findNewEvent(s_2prime,sr,p,Q)

inst = 1000
instance_file = "/Users/meg/repos/cgshop_competition/challenge_instances/data/images/euro-night-" + str(inst).zfill(7) + ".instance"
vertices = readdata(instance_file)

Q = dict([(v,set()) for v in vertices])
Q = SortedDict(Q.items())

T = blist()

all_possible_edges = set()
for pt in vertices:
    for ptB in vertices:
        if ptB > pt:
            all_possible_edges.add(Segment(pt, ptB))
            Q[pt].add(Segment(pt,ptB))

# for q,S in Q.items():
#     print(q)
#     for s in S:
#         print(s)

# T = blist(all_possible_edges)
intCount = 0

while len(Q) != 0:
    p, U = Q.popitem(0)
    # print("handling point "+ str(p))
    # for u in U:
    #     print(u)
    handleEventPoint(p, U, T, Q)
    # print(p)
    # for s in U:
    #     print(s)
print(intCount)



# lines = [[(e.A.x,e.A.y), (e.B.x, e.B.y)] for e in all_possible_edges]
# # print(lines)
# lc = mc.LineCollection(lines, linewidths=2)
# fig, ax = plt.subplots()
# ax.add_collection(lc)
# ax.autoscale()
# ax.margins(0.1)
# plt.show()

# count = 0
# intPts = set()
# for seg1 in all_possible_edges:
#     for seg2 in all_possible_edges:
#         if seg1.A != seg2.A and seg1.B != seg2.B and seg1.A != seg2.B and seg1.B != seg2.A:
#             if seg1.intersects(seg2):
#                 # print(str(seg1)+" intersects with "+str(seg2))
#                 # count += 1
#                 intPts.add(seg1.intersectionPoint(seg2))
#
# print("there were " + str(len(intPts)) + " segment intersections")
# for p in intPts:
#     print(p)
