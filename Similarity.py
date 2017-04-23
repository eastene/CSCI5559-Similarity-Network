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


def measure(distances):
    # average each row
    means = [sum(x) / len(x) for x in distances]
    mu = 0.5
    W = [[0 for i in range(len(distances))] for j in range(len(distances))]

    # compute similarities for each relation i -> j
    for i in range(len(distances) - 1):
        # each row is 1 less than total nodes since a node is not related to itself
        for j in range(i + 1, len(distances) - 1):
            epsilon = (means[i] + means[j] + distances[i][j]) / 3
            W[i][j] = math.exp(-math.pow(distances[i][j], 2) / (mu * epsilon))
    return W
