# Functions used in creation of similarity network

import math


def distance(i, j):
    # start at 1 to skip patient id
    dist = 0
    for x in range(1, len(i)):
        dist += math.pow(float(i[x]) - float(j[x]), 2)
    return math.sqrt(dist)


def initialDistance(ids, patients):
    """
    euclidean distance between all patients in network
    :param patients: patient data
    :return: distance matrix (upper triangular)
    """
    dist = 0
    buffer = []
    for i in range(len(patients)):
        for j in range(i + 1, len(patients)):
            dist = distance(patients[i], patients[j])
            buffer.append({'from': ids[i], 'to': ids[j], 'mag': dist})
    return buffer


def measure(ids, distances):
    """
    compute the similarity between all nodes
    :param distances: initial distances
    :return: similarity matrix (upper triangular)
    """
    # average each row
    means = [sum(x) / len(x) for x in distances]
    mu = 0.5
    W = 0
    buffer = []
    # compute similarities for each relation i -> j
    for i in range(len(distances) - 1):
        # each row is 1 less than total nodes since a node is not related to itself
        for j in range(i + 1, len(distances) - 1):
            epsilon = (means[i] + means[j] + distances[i][j]) / 3
            W = math.exp(-math.pow(distances[i][j], 2) / (mu * epsilon))
            buffer.append({'relID': ids[i][j], 'mag': W})
    return buffer
