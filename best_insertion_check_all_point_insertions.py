import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import time
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
    with open(filename, 'r') as f:
        lines = f.readlines()

    for l in lines:
        l.strip()
        if (len(l) != 0 and l[0] != '#'):
            [i, x, y] = l.split()
            list_data.append([int(x),int(y)])

    data = np.asarray(list_data)
    return data

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

start = time.time()

for inst in [10,15,20,25,30,35,40,45,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
# for inst in [10,15,20,25,30,35]:
    start_inst = time.time()

    instance_file = "/Users/meg/repos/cgshop_competition/challenge_instances/data/images/euro-night-" + str(inst).zfill(7) + ".instance"
    max_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/all_insertions/submission/euro-night-"+str(inst).zfill(7)+".maximum.solution"
    max_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/all_insertions/plots/euro-night-"+str(inst).zfill(7)+".maximum.png"
    min_solution_file =  "/Users/meg/repos/cgshop_competition/solutions/all_insertions/submission/euro-night-"+str(inst).zfill(7)+".minimum.solution"
    min_graphic_file = "/Users/meg/repos/cgshop_competition/solutions/all_insertions/plots/euro-night-"+str(inst).zfill(7)+".minimum.png"

    vertices = readdata(instance_file)
    hull = ConvexHull(vertices)

    start = time.time()

    current_boundary = hull.vertices.tolist()

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
        max_area = 99999999999
        opt_boundary = []
        test_boundary = current_boundary[:]
        for i in range(len(in_complex)):
            if in_complex[i] == 0:
                for j in range(len(current_boundary)):
                    test_boundary.insert(j, i)
                    legal = 0
                    line_A = vertices[test_boundary[j-1],:]
                    line_B = vertices[test_boundary[j],:]
                    line_C = vertices[test_boundary[j+1],:]
                    for k in range(len(test_boundary)-1):
                        test_A = vertices[test_boundary[k],:]
                        test_B = vertices[test_boundary[k+1],:]
                        if k == j-2:
                            if (intersect(line_B, line_C, test_A, test_B)):
                                legal = 1
                                break
                        elif k == j+1:
                            if (intersect(line_A, line_B, test_A, test_B)):
                                legal = 1
                                break
                        elif k!=j-1 and k!=j:
                            if (intersect(line_A, line_B, test_A, test_B) or intersect(line_B, line_C, test_A, test_B)):
                                legal = 1
                                break
                    if legal == 0:
                        curr_area = area(vertices,test_boundary)
                        if curr_area < max_area:
                            max_area = curr_area
                            # print("new max = " + str(max_area))
                            opt_boundary = test_boundary[:]
                    test_boundary.pop(j)
        current_boundary = opt_boundary[:]
        for pt in current_boundary:
            in_complex[pt] = 1

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

    current_boundary = hull.vertices.tolist()

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
        opt_boundary = []
        test_boundary = current_boundary[:]
        for i in range(len(in_complex)):
            if in_complex[i] == 0:
                for j in range(len(current_boundary)):
                    test_boundary.insert(j, i)
                    legal = 0
                    line_A = vertices[test_boundary[j-1],:]
                    line_B = vertices[test_boundary[j],:]
                    line_C = vertices[test_boundary[j+1],:]
                    for k in range(len(test_boundary)-1):
                        test_A = vertices[test_boundary[k],:]
                        test_B = vertices[test_boundary[k+1],:]
                        if k == j-2:
                            if (intersect(line_B, line_C, test_A, test_B)):
                                legal = 1
                                break
                        elif k == j+1:
                            if (intersect(line_A, line_B, test_A, test_B)):
                                legal = 1
                                break
                        elif k!=j-1 and k!=j:
                            if (intersect(line_A, line_B, test_A, test_B) or intersect(line_B, line_C, test_A, test_B)):
                                legal = 1
                                break
                    if legal == 0:
                        curr_area = area(vertices,test_boundary)
                        if curr_area > max_area:
                            max_area = curr_area
                            # print("new max = " + str(max_area))
                            opt_boundary = test_boundary[:]
                    test_boundary.pop(j)
        current_boundary = opt_boundary[:]
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
