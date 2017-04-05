# Interface for the SNF

import DBConnection, Similarity
import queue

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
        # priority queue to hold all distances, then keep only the nearest k
        neighbor_dist = queue.PriorityQueue()
        print("Computing initial distances...")
        # get list of patient ids
        nodes = self.conn.getPatientIDList()
        for i in range(len(nodes)):
            # must use [0] subscript to retrieve Patient_ID from the list of attributes (of len 1)
            node_i = self.conn.getPatient(nodes[i][0])
            for j in range(i):
                    node_j = self.conn.getPatient(nodes[j][0])
                    # using [0] from each node to access property list
                    dist = Similarity.distance(list(node_i.values()), list(node_j.values()))
                    neighbor_dist.put((dist, nodes[j][0]))

            for nn in range(k):
                # set relations for each of the k nearest neighbors to node i
                if not neighbor_dist.empty():
                    dist, n_id = neighbor_dist._get()
                    self.conn.addRelation(nodes[i][0], n_id, dist)


n = Network()
n.computeDistances(5)