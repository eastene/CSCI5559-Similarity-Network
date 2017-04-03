# Interface for the SNF

import DBConnection, Similarity

class Network:
    def __init__(self):
        self.conn = DBConnection.DBConnection()

    def __del__(self):
        del self.conn

    def computeDistances(self):
        # get list of patient ids
        print("Computing initial distances...")
        nodes = self.conn.getPatientIDList()
        for id_i in nodes:
            node_i = self.conn.getPatient(id_i[0])
            for id_j in nodes:
                if id_i != id_j:
                    node_j = self.conn.getPatient(id_j[0])
                    # using [0] from each node to access property list
                    dist = Similarity.distance(list(node_i.values()), list(node_j.values()))
                    self.conn.addRelation(id_i[0], id_j[0], dist)


n = Network()
n.computeDistances()