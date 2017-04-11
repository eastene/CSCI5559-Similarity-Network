# Interface for the SNF

import DBConnection, Similarity

class Network:
    def __init__(self):
        self.conn = DBConnection.DBConnection()

    def __del__(self):
        del self.conn

    def computeDistances(self, k=20):
        '''
        Compute the initial distances between a node and its nearest k neighbors
        :param k: number of nearest neighbors to consider (default = 20)
        :return: 
        '''
        # queue to hold all distances, (possibly used later in finding the average dist to the k nearest)
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



n = Network()
n.computeDistances(5)