# Parse files for data used to create SNF
# Potentailly add support for more file types

import DBConnection, Similarity
import csv, threading

class FileParser:

    files_read = 0

    def __init__(self, verbose=False):
        # establish connection to db
        self.conn = DBConnection.DBConnection()
        self.verbose = verbose

    def __del__(self):
        # close db connection
        del self.conn

    def addAttributes(self, fileName, delimiter):
        with open(fileName, 'r') as f_in:
            if self.verbose:
                print("Parsing File " + str(self.files_read) + " ...", end=' ', flush=True)
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
            if self.verbose:
                print("Done.")

    def allocateNodes(self, fileName, delimiter):
        with open(fileName, 'r') as f_in:
            if self.verbose:
                print("Parsing File 1...", end=' ', flush=True)
            # read csv in Dictionary format
            reader = csv.DictReader(f_in, delimiter=delimiter)
            # read in each node
            self.conn.allocatePatients(reader)
            if self.verbose:
                print("        Done.")

    def parseCreatorFile(self, fileName, delimiter):
        """
        Parse first data type to create the nodes for the graph
        :param fileName: file from which to read (.csv)
        :param delimit: delimiter of file
        :return: none
        """
        task = threading.Thread(target=self.allocateNodes(fileName, delimiter))
        task.start()
        # new reader to measure the distances
        with open(fileName, 'r') as f_in:
            if self.verbose:
                print("Calculating Distances...", end=" ", flush=True)
            reader = csv.reader(f_in, delimiter=delimiter)
            # skip headers
            next(reader)
            patients = [row for row in reader if row != []]
            distances = Similarity.initialDistance(patients)
            ids = [row[0] for row in patients]
            # wait until all new nodes are allocated
            task.join()
            if self.verbose:
                print(" Done.")
                print("Writing Distances...", end=" ", flush=True)
            buffer = [{'from': ids[i], 'to': ids[j], 'mag': distances[i][j]} for i in range(len(ids))
                      for j in range(i + 1, len(ids))]
            self.conn.addRelationsFromBuffer(buffer)
            self.files_read += 1
            if self.verbose:
                print("     Done.")

    def parseNewDataType(self, fileName, delimiter):
        """
        Parse additional data types for existing nodes in the graph
        :param fileName: file from which to read (.csv)
        :param delimit: delimiter of file
        :return: none
        """
        task = threading.Thread(target=self.addAttributes(fileName, delimiter))
        task.start()
        with open(fileName, 'r') as f_in:
            if self.verbose:
                print("Calculating Distances for Data Type " + str(self.files_read) + " ...", end=" ", flush=True)
            reader = csv.reader(f_in, delimiter=delimiter)
            # skip headers
            next(reader)
            patients = [row for row in reader if row != []]
            distances = Similarity.initialDistance(patients)
            ids = [row[0] for row in patients]
            task.join()
            # write initial distances
            self.conn.addRelationsFromBuffer(ids, distances, "Similarity " + str(self.files_read))
            self.files_read += 1
            if self.verbose:
                print("Done.")
