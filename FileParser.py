# Parse files for data used to create SNF
# Potentailly add support for more file types

import DBConnection
import csv

class FileParser:

    def __init__(self):
        # establish connection to db
        self.conn = DBConnection.DBConnection()

    def __del__(self):
        # close db connection
        del self.conn

    def parseCreatorFile(self, fileName):
        with open(fileName, 'r') as f_in:
            # read csv in Dictionary format
            reader = csv.DictReader(f_in)
            # read in each node
            for row in reader:
                # create the node for the patient with the given attributes
                self.conn.allocatePatient(row)

    def parseNewDataType(self, fileName):
        with open(fileName, 'r') as f_in:
            # read csv in Dictionary format
            reader = csv.DictReader(f_in)
            # read in new data type for each node
            for row in reader:
                # extract patient ID to identify patient, but do not add new id
                id = row['Patient_ID']
                del row['Patient_ID']
                # add new attributes
                self.conn.addAttributes(id, row)