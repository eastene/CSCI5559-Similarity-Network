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
    for val in i:
        if val != "Patient_ID" and val in j:
            dist += (float(i[val]) - float(j[val])) ** 2
    return math.sqrt(dist)

def avgDistToNeighbor(i):
    '''
    Avg. euclidean distance between node i and its neighbors
    :param i: 
    :return: 
    '''

def measure(xi_N, xj_N, p_i_j):
    mean_xi_N = sum(int(i[1]) for i in xi_N) / len(xi_N)
    mean_xj_N = sum(int(j[1]) for j in xj_N) / len(xj_N)
    mu = 0.5
    epsilon = (mean_xi_N + mean_xj_N + p_i_j) / 3
    W = math.exp(-(math.pow(p_i_j, 2)) / (mu * epsilon))

    return W
