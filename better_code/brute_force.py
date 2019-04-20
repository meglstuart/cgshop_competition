#!/usr/bin/env python3

from FindIntersections import findIntersections
from Hashable2dGeometry import Point, Segment, Orientation
from sortedcontainers import SortedDict
import itertools
import time
import numpy as np
import matplotlib.pyplot as plt

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

def dictFromBoundaryList(pt_list, current_boundary):
    curr_bd_dict = dict([(p,set()) for p in pt_list])
    curr_bd_dict = SortedDict(curr_bd_dict.items())

    for i in range(len(current_boundary)):
        if pt_list[current_boundary[(i+1)%len(current_boundary)]] > pt_list[current_boundary[i]]:
            curr_bd_dict[pt_list[current_boundary[i]]].add(Segment(pt_list[current_boundary[i]],pt_list[current_boundary[(i+1)%len(current_boundary)]]))
        else:
            curr_bd_dict[pt_list[current_boundary[(i+1)%len(current_boundary)]]].add(Segment(pt_list[current_boundary[i]],pt_list[current_boundary[(i+1)%len(current_boundary)]]))

    return curr_bd_dict

# for inst in [10,15,20,25,30,35,40,45,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
for inst in [35,40,45,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
    start = time.time()
    end = time.time()
    cutoff = 10
    instance_file = "/Users/meg/repos/cgshop_competition/challenge_instances/data/images/euro-night-" + str(inst).zfill(7) + ".instance"
    max_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/brute_force/submission/euro-night-"+str(inst).zfill(7)+".maximum.solution"
    max_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/brute_force/plots/euro-night-"+str(inst).zfill(7)+".maximum.png"
    min_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/brute_force/submission/euro-night-"+str(inst).zfill(7)+".minimum.solution"
    min_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/brute_force/plots/euro-night-"+str(inst).zfill(7)+".minimum.png"

    pt_list, vertices = readdata(instance_file)

    boundary = [i for i in range(1,len(pt_list))]

    max_area = 0
    min_area = 99999999999999

    found_valid_bd = False

    for bd in itertools.permutations(boundary):
        if (end-start) > cutoff and found_valid_bd:
            break
        bd = [0] + list(bd) #choose 0 to be our pivot, cyclic permutations don't give new boundaries
        # print("testing boundary " + str(bd))
        bd_dict = dictFromBoundaryList(pt_list, bd)
        intersection = findIntersections(bd_dict)
        if intersection == 0:
            found_valid_bd = True
            curr_area = area(vertices,bd)
            if curr_area > max_area:
                max_area = curr_area
                max_bd = list(bd)
                print("new max = "+ str(max_area))
            if curr_area < min_area:
                min_area = curr_area
                min_bd = list(bd)
                print("new min = "+ str(min_area))
        end = time.time()




    with open(min_solution_file, 'w') as out:
        out.write("# time = " + str(end-start) + "\n")
        out.write("# area = " + str(area(vertices, min_bd)) + "\n")
        for vert in min_bd:
            out.write(str(vert) + "\n")

    plt.plot(vertices[:,0],vertices[:,1], "ro")
    min_bd.append(min_bd[0])
    plt.plot(vertices[min_bd, 0], vertices[min_bd, 1], 'k-')
    plt.savefig(min_graphic_file)
    plt.clf()


    with open(max_solution_file, 'w') as out:
        out.write("# time = " + str(end-start) + "\n")
        out.write("# area = " + str(area(vertices, max_bd)) + "\n")
        for vert in max_bd:
            out.write(str(vert) + "\n")

    plt.plot(vertices[:,0],vertices[:,1], "ro")
    max_bd.append(max_bd[0])
    plt.plot(vertices[max_bd, 0], vertices[max_bd, 1], 'k-')
    plt.savefig(max_graphic_file)
    plt.clf()

    print("Done with instance "+str(inst).zfill(7))
    print("Time = " + str(end-start))
    print("Min area = " + str(area(vertices, min_bd)))
    print("Max area = " + str(area(vertices, max_bd)))
