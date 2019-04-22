#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from FindIntersections import findIntersections
import time
from Hashable2dGeometry import Point, Segment, Orientation
from sortedcontainers import SortedDict
from copy import deepcopy
from blist import blist


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

for inst in [10,15,20,25,30,35,40,45,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
# for inst in [60,70,80,90,100,   200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
# for inst in [10,15,20,25,30,35,40,45,50]:

# for inst in [10]:

    start_inst = time.time()

    instance_file = "/Users/meg/repos/cgshop_competition/challenge_instances/data/images/euro-night-" + str(inst).zfill(7) + ".instance"
    max_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/untangling/submission/euro-night-"+str(inst).zfill(7)+".maximum.solution"
    max_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/untangling/plots/euro-night-"+str(inst).zfill(7)+".maximum.png"
    min_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/untangling/submission/euro-night-"+str(inst).zfill(7)+".minimum.solution"
    min_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/untangling/plots/euro-night-"+str(inst).zfill(7)+".minimum.png"

    pt_list, vertices = readdata(instance_file)
    hull = ConvexHull(vertices)

    start = time.time()

    current_boundary = blist(hull.vertices.tolist())


    # if pt_list[current_boundary[-1]] > pt_list[current_boundary[0]]:
    #     curr_bd_dict[pt_list[current_boundary[0]]].add(Segment(pt_list[current_boundary[0]],pt_list[current_boundary[-1]]))
    # else:
    #     curr_bd_dict[pt_list[current_boundary[-1]]].add(Segment(pt_list[current_boundary[0]],pt_list[current_boundary[-1]]))


    in_complex = np.zeros_like(vertices[:,0])
    for pt in current_boundary:
        in_complex[pt] = 1

    # not_in_complex = []
    num_left = 0;
    for i in range(len(in_complex)):
        if in_complex[i] == 0:
            num_left+=1

    # print(current_boundary)
    # print(in_complex)
    # print(not_in_complex)
    for n in range(num_left):
        max_area = 99999999999999
        # opt_boundary = []
        test_boundary = current_boundary
        # test_bd_dict = dictFromBoundaryList(pt_list,current_boundary) #Slightly faster than copying every time a new max is found
        for i in range(len(in_complex)):
            if in_complex[i] == 0:
                for j in range(len(current_boundary)):

                    # old_seg = Segment(pt_list[test_boundary[j-1]],pt_list[test_boundary[j%len(test_boundary)]])
                    # test_bd_dict[pt_list[test_boundary[j%len(test_boundary)]]].discard(old_seg)
                    # test_bd_dict[pt_list[test_boundary[j-1]]].discard(old_seg)

                    test_boundary.insert(j, i)

                    # new_seg1 = Segment(pt_list[test_boundary[j-1]],pt_list[test_boundary[j]])
                    # if pt_list[test_boundary[j-1]] > pt_list[test_boundary[j]]:
                    #     test_bd_dict[pt_list[test_boundary[j]]].add(new_seg1)
                    # else:
                    #     test_bd_dict[pt_list[test_boundary[j-1]]].add(new_seg1)
                    #
                    # new_seg2 = Segment(pt_list[test_boundary[(j+1)%len(test_boundary)]],pt_list[test_boundary[j]])
                    # if pt_list[test_boundary[(j+1)%len(test_boundary)]] > pt_list[test_boundary[j]]:
                    #     test_bd_dict[pt_list[test_boundary[j]]].add(new_seg2)
                    # else:
                    #     test_bd_dict[pt_list[test_boundary[(j+1)%len(test_boundary)]]].add(new_seg2)
                    # intersections = findIntersections(SortedDict(test_bd_dict))

                    if True:
                        curr_area = area(vertices,test_boundary)
                        if curr_area < max_area:
                            max_area = curr_area
                            # print("new max = " + str(max_area))
                            current_boundary = blist(test_boundary)
                    # test_bd_dict[pt_list[test_boundary[j-1]]].discard(new_seg1)
                    # test_bd_dict[pt_list[test_boundary[j]]].discard(new_seg1)
                    # test_bd_dict[pt_list[test_boundary[j]]].discard(new_seg2)
                    # test_bd_dict[pt_list[test_boundary[(j+1)%len(test_boundary)]]].discard(new_seg2)
                    test_boundary.pop(j)
                    # if pt_list[test_boundary[j-1]] > pt_list[test_boundary[j%len(test_boundary)]]:
                    #     test_bd_dict[pt_list[test_boundary[j%len(test_boundary)]]].add(old_seg)
                    # else:
                    #     test_bd_dict[pt_list[test_boundary[j-1]]].add(old_seg)
        for pt in current_boundary:
            in_complex[pt] = 1

        if (n%10):
            #untangle

    end = time.time()
    # print("time = "+str(end-start))
    # print(current_boundary)
    with open(min_solution_file, 'w') as out:
        out.write("# time = " + str(end-start) + "\n")
        out.write("# area = " + str(area(vertices, current_boundary)) + "\n")
        for vert in current_boundary:
            out.write(str(vert) + "\n")

    # print(area(vertices, current_boundary))
    plt.plot(vertices[:,0],vertices[:,1], "ro")
    current_boundary.append(current_boundary[0])
    plt.plot(vertices[current_boundary, 0], vertices[current_boundary, 1], 'k-')
    plt.savefig(min_graphic_file)
    plt.clf()



    start = time.time()

    current_boundary = blist(hull.vertices.tolist())


    # if pt_list[current_boundary[-1]] > pt_list[current_boundary[0]]:
    #     curr_bd_dict[pt_list[current_boundary[0]]].add(Segment(pt_list[current_boundary[0]],pt_list[current_boundary[-1]]))
    # else:
    #     curr_bd_dict[pt_list[current_boundary[-1]]].add(Segment(pt_list[current_boundary[0]],pt_list[current_boundary[-1]]))


    in_complex = np.zeros_like(vertices[:,0])
    for pt in current_boundary:
        in_complex[pt] = 1

    # not_in_complex = []
    num_left = 0;
    for i in range(len(in_complex)):
        if in_complex[i] == 0:
            num_left+=1

    # print(current_boundary)
    # print(in_complex)
    # print(not_in_complex)
    for n in range(num_left):
        max_area = 0
        # opt_boundary = []
        test_boundary = current_boundary
        # test_bd_dict = dictFromBoundaryList(pt_list,current_boundary) #Slightly faster than copying every time a new max is found
        for i in range(len(in_complex)):
            if in_complex[i] == 0:
                for j in range(len(current_boundary)):

                    # old_seg = Segment(pt_list[test_boundary[j-1]],pt_list[test_boundary[j%len(test_boundary)]])
                    # test_bd_dict[pt_list[test_boundary[j%len(test_boundary)]]].discard(old_seg)
                    # test_bd_dict[pt_list[test_boundary[j-1]]].discard(old_seg)

                    test_boundary.insert(j, i)

                    # new_seg1 = Segment(pt_list[test_boundary[j-1]],pt_list[test_boundary[j]])
                    # if pt_list[test_boundary[j-1]] > pt_list[test_boundary[j]]:
                    #     test_bd_dict[pt_list[test_boundary[j]]].add(new_seg1)
                    # else:
                    #     test_bd_dict[pt_list[test_boundary[j-1]]].add(new_seg1)
                    #
                    # new_seg2 = Segment(pt_list[test_boundary[(j+1)%len(test_boundary)]],pt_list[test_boundary[j]])
                    # if pt_list[test_boundary[(j+1)%len(test_boundary)]] > pt_list[test_boundary[j]]:
                    #     test_bd_dict[pt_list[test_boundary[j]]].add(new_seg2)
                    # else:
                    #     test_bd_dict[pt_list[test_boundary[(j+1)%len(test_boundary)]]].add(new_seg2)
                    # intersections = findIntersections(SortedDict(test_bd_dict))

                    if True:
                        curr_area = area(vertices,test_boundary)
                        if curr_area > max_area:
                            max_area = curr_area
                            # print("new max = " + str(max_area))
                            current_boundary = blist(test_boundary)
                    # test_bd_dict[pt_list[test_boundary[j-1]]].discard(new_seg1)
                    # test_bd_dict[pt_list[test_boundary[j]]].discard(new_seg1)
                    # test_bd_dict[pt_list[test_boundary[j]]].discard(new_seg2)
                    # test_bd_dict[pt_list[test_boundary[(j+1)%len(test_boundary)]]].discard(new_seg2)
                    test_boundary.pop(j)
                    # if pt_list[test_boundary[j-1]] > pt_list[test_boundary[j%len(test_boundary)]]:
                    #     test_bd_dict[pt_list[test_boundary[j%len(test_boundary)]]].add(old_seg)
                    # else:
                    #     test_bd_dict[pt_list[test_boundary[j-1]]].add(old_seg)
        for pt in current_boundary:
            in_complex[pt] = 1

    end = time.time()
    # print("time = "+str(end-start))
    # print(current_boundary)
    with open(max_solution_file, 'w') as out:
        out.write("# time = " + str(end-start) + "\n")
        out.write("# area = " + str(area(vertices, current_boundary)) + "\n")
        for vert in current_boundary:
            out.write(str(vert) + "\n")

    # print(area(vertices, current_boundary))
    plt.plot(vertices[:,0],vertices[:,1], "ro")
    current_boundary.append(current_boundary[0])
    plt.plot(vertices[current_boundary, 0], vertices[current_boundary, 1], 'k-')
    plt.savefig(max_graphic_file)
    plt.clf()

    print("Done with instance number " + str(inst).zfill(7) )
    print("Time for this instance = " + str(end - start_inst))
