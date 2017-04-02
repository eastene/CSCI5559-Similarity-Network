# Interface for the SNF

import DBConnection

class Network:
    def __init__(self):
        self.conn = DBConnection.DBConnection()

    def __del__(self):
        del self.conn