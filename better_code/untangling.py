#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from FindIntersectionsReworked import findIntersections
import time
from Hashable2dGeometry import Point, Segment, Orientation
from sortedcontainers import SortedDict
from copy import deepcopy
from blist import blist
from random import shuffle


def perpdot(p1, p2):
    return p1[0]*p2[1]-p1[1]*p2[0]

def area(points, boundary):
    N = len(boundary)
    twicearea = perpdot(points[boundary[0],:], points[boundary[N-1],:])
    for i in range(1,N):
        twicearea += perpdot(points[boundary[i],:], points[boundary[i-1],:])
    return abs(twicearea/2)

def readdata(filename):
    list_data = list()
    point_list = list()
    with open(filename, 'r') as f:
        lines = f.readlines()

    for l in lines:
        l.strip()
        if (len(l) != 0 and l[0] != '#'):
            [i, x, y] = l.split()
            list_data.append([int(x),int(y)])
            point_list.append(Point(int(x),int(y)))


    data = np.asarray(list_data)
    return point_list, data

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def dictFromBoundaryList(pt_list, current_boundary):
    curr_bd_dict = dict([(p,set()) for p in pt_list])
    curr_bd_dict = SortedDict(curr_bd_dict.items())

    for i in range(len(current_boundary)):
        if pt_list[current_boundary[(i+1)%len(current_boundary)]] > pt_list[current_boundary[i]]:
            curr_bd_dict[pt_list[current_boundary[i]]].add(Segment(pt_list[current_boundary[i]],pt_list[current_boundary[(i+1)%len(current_boundary)]]))
        else:
            curr_bd_dict[pt_list[current_boundary[(i+1)%len(current_boundary)]]].add(Segment(pt_list[current_boundary[i]],pt_list[current_boundary[(i+1)%len(current_boundary)]]))

    return curr_bd_dict

# start = time.time()

# for inst in [10,15,20,25,30,35,40,45,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
# for inst in [60,70,80,90,100,   200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
# for inst in [10,15,20,25,30,35,40,45,50]:

for inst in [10]:

    start_inst = time.time()

    instance_file = "/Users/meg/repos/cgshop_competition/challenge_instances/data/images/euro-night-" + str(inst).zfill(7) + ".instance"
    max_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/untangling/submission/euro-night-"+str(inst).zfill(7)+".maximum.solution"
    max_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/untangling/plots/euro-night-"+str(inst).zfill(7)+".maximum.png"
    min_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/untangling/submission/euro-night-"+str(inst).zfill(7)+".minimum.solution"
    min_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/untangling/plots/euro-night-"+str(inst).zfill(7)+".minimum.png"

    pt_list, vertices = readdata(instance_file)
    # hull = ConvexHull(vertices)

    start = time.time()

    boundary = [i for i in range(1,len(pt_list))]



    # for i in range(10):
    shuffle(boundary)
    # while(findIntersections(bd_dict)):
    bd_dict = dictFromBoundaryList(pt_list, boundary)
    (C,E) = findIntersections(bd_dict)
    if(len(E) != 0):
        print("type 2 intersection")
    else:
        print("type 1 or 3 intersection")
    print(boundary)


    end = time.time()
    # print("time = "+str(end-start))
    # print(current_boundary)
    # with open(min_solution_file, 'w') as out:
    #     out.write("# time = " + str(end-start) + "\n")
    #     out.write("# area = " + str(area(vertices, current_boundary)) + "\n")
    #     for vert in current_boundary:
    #         out.write(str(vert) + "\n")
    #
    # # print(area(vertices, current_boundary))
    # plt.plot(vertices[:,0],vertices[:,1], "ro")
    # current_boundary.append(current_boundary[0])
    # plt.plot(vertices[current_boundary, 0], vertices[current_boundary, 1], 'k-')
    # plt.savefig(min_graphic_file)
    # plt.clf()
    #
    #
    #
    # with open(max_solution_file, 'w') as out:
    #     out.write("# time = " + str(end-start) + "\n")
    #     out.write("# area = " + str(area(vertices, current_boundary)) + "\n")
    #     for vert in current_boundary:
    #         out.write(str(vert) + "\n")
    #
    # # print(area(vertices, current_boundary))
    # plt.plot(vertices[:,0],vertices[:,1], "ro")
    # current_boundary.append(current_boundary[0])
    # plt.plot(vertices[current_boundary, 0], vertices[current_boundary, 1], 'k-')
    # plt.savefig(max_graphic_file)
    # plt.clf()

    print("Done with instance number " + str(inst).zfill(7) )
    print("Time for this instance = " + str(end - start_inst))
