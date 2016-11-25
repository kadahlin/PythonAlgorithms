#Kyle Dahlin - Graham Scan algorithm using plane sweep and matrix multiplication

#Implementation of the graham scan algorithm for finding the convex hull
#for a set of points given as a list of of (x,y) tuples

import sys
import os.path

def graham_scan(filename):
    points = list_of_points(filename)
    num_points = len(points)

    #sort by x element: O(n log n)
    #left most element is points[0] and the right most is points[num_points - 1]
    points.sort()
    #print(points)

    #list (stack) that will hold the values that are located above
    #the left most and right most points
    top_points = top_half(points, num_points)
    bottom_points = bottom_half(points, num_points)

    #The output is clockwise from the left most point so combine the entire
    #top half of the points with the bottom half (stripped of the left most and
    #right most)

    convex_hull = top_points + list(reversed(bottom_points))

    print(convex_hull)

#Input is tuples that are pairs of (x, y) points,
#Output is the determinant of the three points.
#If the output is < 0 then we have a left turn and the point
#will be added to the convex hull list for the points above the endpoints.
#If the output is > 0 then we have a right turn which is the condition for the
#bottom half of the points.
def det(one, two, three):
    part_one = one[0] * (two[1] - three[1])
    part_two = one[1] * (two[0] - three[0])
    part_three = (two[0] * three[1] - two[1] * three[0])
    d =  part_one - part_two + part_three
    #print("the det for {} and {} and {} is {}".format(one, two, three, d))
    return d

#Read the points from a file where every line is two numbers xy, seperated by a
#tab character.
#Input is a string containing a filename with the conditions specified above
def list_of_points(filename):
    points = []
    with open(filename) as file:
        for line in file.readlines():
            coord = line.strip().split("\t")
            points.append((int(coord[0]), int(coord[1])))
    return points

#Input is the list of coordinate (x, y) tuples.
#Output is a list of tuples that are both part of the convex hull and above
#the left most point and right most point

def top_half(points, length):
    top_points = []

    #Value that will be used to see if a point is above or below the two end points
    min_y = min(points[0][1], points[length - 1][1])

    for i in range(length):
        if points[i][1] < min_y: #point is below the end points and is ignored
                continue
        if len(top_points) < 2: #there must be at least two in the top section
                top_points.append(points[i])
                continue
        if det(top_points[len(top_points) - 2], top_points[len(top_points) - 1], points[i]) < 0:
            top_points.append(points[i])
        else:
            top_points.pop()
            top_points.append(points[i])
        current = len(top_points)

        #check to make sure that the new shape formed by this point is not concave
        #if the shape is concave, backtrack and pop points until it is not
        while current > 3:
            if(det(top_points[current - 3], top_points[current - 2], top_points[current - 1])) > 0:
                top_points.pop(current - 2)
                current -= 1
            else:
                break
    return top_points

#Input is the list of coordinate (x, y) tuples.
#Output is a list of tuples that are both part of the convex hull and below
#the left most point and right most point
def bottom_half(points, length):
    bottom_points = []

    #Value that will be used to see if a point is above or below the two end points
    min_y = min(points[0][1], points[length - 1][1])

    for i in range(length):
        if len(bottom_points) < 2: #there must be at least two in the top section
                bottom_points.append(points[i])
                continue
        if points[i][1] >= min_y: #point is above the end points and is ignored
                continue
        if det(bottom_points[len(bottom_points) - 2], bottom_points[len(bottom_points) - 1], points[i]) > 0:
            bottom_points.append(points[i])
        else:
            bottom_points.pop()
            bottom_points.append(points[i])

        #check to make sure that the new shape formed by this point is not concave
        #if the shape is concave, backtrack and pop points until it is not
        current = len(bottom_points)
        while current > 3:
            if(det(bottom_points[current - 3], bottom_points[current - 2], bottom_points[current - 1])) < 0:
                bottom_points.pop(current - 2)
                current -= 1
            else:
                break
    return bottom_points


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("A filename was not specified, exiting.")
        sys.exit()
    if not os.path.isfile(sys.argv[1]):
        print("Could not see the specified file, exiting.")
        sys.exit()
    graham_scan(sys.argv[1])
