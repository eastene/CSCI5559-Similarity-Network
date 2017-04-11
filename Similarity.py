# Functions used in creation of similarity network

import math

def distance(i, j):
    '''
    Squared Euclidean distance between two nodes
    :param i: node i's feature list
    :param j: node j's feature list
    :return: value of distance between nodes i and j
    '''
    dist = 0
    # compare each named attribute in i and j and add to the distance
    for val in i.keys():
        if val != "Patient_ID" and val in j:
            dist += (float(i[val]) - float(j[val])) ** 2
    return math.sqrt(dist)

def avgDistToNeighbor(i):
    '''
    Avg. euclidean distance between node i and its neighbors
    :param i: 
    :return: 
    '''

def measure(i, j):
    dist = distance(i, j)
    avg_dist_i = avgDistToNeighbor(i)
    avg_dist_j = avgDistToNeighbor(j)

    epsilon = (avg_dist_i + avg_dist_j + dist) / 3
    mu = 0.5

    return math.exp(-(dist ** 2) / (epsilon * mu))
