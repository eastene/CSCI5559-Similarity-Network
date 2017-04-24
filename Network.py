# Interface for the SNF

import DBConnection, Similarity


class Network:

    def __init__(self, verbose=False):
        self.conn = DBConnection.DBConnection()
        self.verbose = verbose

    def __del__(self):
        del self.conn

    def computeSimilarity(self):
        """
        compute the similarity between nodes using the distances computed earlier
        :return: none
        """
        if self.verbose:
            print("Computing similarities ...", end=" ", flush=True)
        # 2d array to hold all distances
        distances = []
        # get list of patient ids
        nodes = self.conn.getSortedIDList()
        for i in range(len(nodes)):
            # compute average distance to neighbors for node i
            xi_N = self.conn.getPatientRelations(nodes[i][0])
            distances.append([x[1] for x in xi_N])
        # compute the similarities
        W = Similarity.measure(distances)
        # write the similarities to disk
        self.conn.updateRelationsFromBuffer(nodes, W)
        if self.verbose:
            print("Done.")
