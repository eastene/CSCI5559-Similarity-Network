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

def measure(distances):

    # average each row
    means = [sum(x) / len(x) for x in distances]
    mu = 0.5
    row = []
    W = []
    # compute similarities for each relation i -> j
    for i in range(len(distances)):
        # each row is 1 less than total nodes since a node is not related to itself
        for j in range(i + 1, len(distances) - 1):
            epsilon = (means[i] + means[j] + distances[i][j]) / 3
            row.append(math.exp(-(math.pow(distances[i][j], 2)) / (mu * epsilon)))
        W.append(row)
    return W
