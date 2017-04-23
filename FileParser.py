# Parse files for data used to create SNF
# Potentailly add support for more file types

import DBConnection, Similarity
import csv

class FileParser:

    files_read = 0

    def __init__(self):
        # establish connection to db
        self.conn = DBConnection.DBConnection()

    def __del__(self):
        # close db connection
        del self.conn

    def parseCreatorFile(self, fileName, delimiter):
        """
        Parse first data type to create the nodes for the graph
        :param fileName: file from which to read (.csv)
        :param delimit: delimiter of file
        :return: none
        """
        with open(fileName, 'r') as f_in:
            print("Parsing File 1 ...", end=' ')
            # read csv in Dictionary format
            reader = csv.DictReader(f_in, delimiter=delimiter)
            # read in each node
            self.conn.allocatePatients(reader)
            f_in.seek(0)
            # new reader to measure the distances
            print("Done.")
            print("Calculating Distances ...",end=" ")
            reader2 = csv.reader(f_in,delimiter=delimiter)
            # skip headers
            next(reader2)
            patients = [row for row in reader2 if row != []]
            distances = Similarity.initialDistance(patients)
            ids = [row[0] for row in patients]
            self.conn.addRelationsFromBuffer(ids, distances, "Similarity 1")
            self.files_read += 1
            print("Done.")

    def parseNewDataType(self, fileName, delimiter):
        """
        Parse additional data types for existing nodes in the graph
        :param fileName: file from which to read (.csv)
        :param delimit: delimiter of file
        :return: none
        """
        with open(fileName, 'r') as f_in:
            print("Parsing File " + str(self.files_read) + " ...", end=' ')
            # read csv in Dictionary format
            reader = csv.DictReader(f_in, delimiter=delimiter)
            # read in new data type for each node
            for row in reader:
                # extract patient ID to identify patient, but do not add new id
                id = row['Patient_ID']
                del row['Patient_ID']
                # add new attributes
                self.conn.addAttributes(id, row)
                self.files_read += 1
            print("Done.")
            print("Calculating Distances for Data Type " + str(self.files_read) + " ...", end=" ")
            reader2 = csv.reader(f_in, delimiter=delimiter)
            # skip headers
            next(reader2)
            patients = [row for row in reader2 if row != []]
            distances = Similarity.initialDistance(patients)
            ids = [row[0] for row in patients]
            # write initial distances
            self.conn.addRelationsFromBuffer(ids, distances, "Similarity " + str(self.files_read))
            self.files_read += 1
            print("Done.")