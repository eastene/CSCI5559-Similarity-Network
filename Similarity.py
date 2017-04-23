# Functions used in creation of similarity network

import math


def distance(i, j):
    # start at 1 to skip patient id
    dist = 0
    for x in range(1, len(i)):
        dist += math.pow(float(i[x]) - float(j[x]), 2)
    return math.sqrt(dist)


def initialDistance(patients):
    """
    euclidean distance between all patients in network
    :param patients: patient data
    :return: distance matrix (upper triangular)
    """
    distances = [[0 for i in range(len(patients))] for j in range(len(patients))]
    for i in range(len(patients)):
        for j in range(i + 1, len(patients)):
            distances[i][j] = distance(patients[i], patients[j])
    return distances


def measure(distances):
    """
    compute the similarity between all nodes
    :param distances: initial distances
    :return: similarity matrix (upper triangular)
    """
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
