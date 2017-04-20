# Interface for the SNF

import DBConnection, Similarity
import math, time

class Network:
    def __init__(self):
        self.conn = DBConnection.DBConnection()

    def __del__(self):
        del self.conn

    def computeDistances(self):
        '''
        Compute the initial distances between a node and its nearest k neighbors
        :param k: number of nearest neighbors to consider (default = 20)
        :return: 
        '''
        # list to hold all distances, (possibly used later in finding the average dist to the k nearest)
        neighbor_dist = []
        print("Computing initial distances...")
        # get list of patient ids
        nodes = self.conn.getPatientIDList()
        for i in range(len(nodes)):
            # must use [0] subscript to retrieve Patient_ID from the list of attributes (of len 1)
            node_i = self.conn.getPatient(nodes[i][0])
            for j in range(i + 1, len(nodes)):
                    node_j = self.conn.getPatient(nodes[j][0])
                    # using [0] from each node to access property list
                    dist = Similarity.distance(node_i, node_j)
                    neighbor_dist.append((nodes[i][0], nodes[j][0], dist))
            # add the relations in bulk
            self.conn.addRelationsFromBuffer(neighbor_dist)
            neighbor_dist.clear()

    def computeSimilarity(self):
        # list to hold all distances, (possibly used later in finding the average dist to the k nearest)
        neighbor_dist = []
        print("Computing similarities...")
        # get list of patient ids
        nodes = self.conn.getPatientIDList()
        mu = 0.5
        for i in range(len(nodes)):
            xi_N = self.conn.getPatientRelations(nodes[i][0])
            tot = 0
            for k in xi_N:
                tot += float(k[0]['magnitude'])
            mean_xi_N = tot/len(xi_N)

            for j in range(i+1, len(nodes)):
                xj_N = self.conn.getPatientRelations(nodes[j][0])
                tot = 0
                for k in xj_N:
                    tot += float(k[0]['magnitude'])
                mean_xj_N = tot / len(xj_N)

                p_i_j = self.conn.getRelation(nodes[i][0], nodes[j][0])[0]['magnitude']
                epsilon = (mean_xi_N + mean_xj_N + p_i_j) / 3
                W = math.exp(-(math.pow(p_i_j, 2))/(mu * epsilon))

                self.conn.updateRelation(nodes[i][0], nodes[j][0], W)

t1 = time.time()
n = Network()
n.computeDistances()
n.computeSimilarity()
print ("Delta: " + time.time() - t1)