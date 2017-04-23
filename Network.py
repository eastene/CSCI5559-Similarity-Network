# Interface for the SNF

import DBConnection, Similarity
import numpy


class Network:

    def __init__(self):
        self.conn = DBConnection.DBConnection()

    def __del__(self):
        del self.conn

    def computeDistances(self):
        '''
        Compute the initial distances between a node and its nearest k neighbors
        :param k: number of nearest neighbors to consider (default = 20)
        :return: none
        '''
        print("Computing initial distances ...", end=" ")
        # list to hold all distances, (possibly used later in finding the average dist to the k nearest)
        neighbor_dist = []
        # get list of patient ids
        ids = self.conn.getSortedIDList()
        # grab a set number of patients at a time, allow using a buffer
        s = 0
        f = len(ids) - 1
        # fetch a range of patients
        nodes = self.conn.getPatientsRange(ids[s][0], ids[f][0])
        for i in range(len(nodes)):
            # must use [0] subscript to retrieve Patient_ID from the list of attributes (of len 1)
            node_i = nodes[i][0]
            for j in range(i + 1, len(nodes)):
                    node_j = nodes[j][0]
                    # using [0] from each node to access property list
                    dist = Similarity.distance(node_i, node_j)
                    neighbor_dist.append((node_i['Patient_ID'], node_j['Patient_ID'], dist))
        # add the relations in bulk
        print("Done.")
        print("Writing Distances ...", end=" ")
        self.conn.addRelationsFromBuffer(neighbor_dist)
        print("Done.")

    def computeSimilarity(self):
        """
        compute the similarity between nodes using the distances computed earlier
        :return: none
        """
        print("Computing similarities ...", end=" ")
        # 2d array to hold all distances
        distances = []

        # get list of patient ids
        nodes = self.conn.getSortedIDList()
        for i in range(len(nodes)):
            # compute average distance to neighbors for node i
            xi_N = self.conn.getPatientRelations(nodes[i][0])
            distances.append([x[1] for x in xi_N])

        W = Similarity.measure(distances)

        print("Done.")
        print("Writing Similarites ...", end=" ")
        self.conn.updateRelationsFromBuffer(nodes, W)
        print("Done.")
