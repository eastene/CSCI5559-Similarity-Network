# Evan Stene
# Class defining a connection to the graph db, and methods to add and update nodes in the network

from neo4j.v1 import GraphDatabase, basic_auth


class DBConnection:

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "dba"))
        self.session = self.driver.session()

    def __del__(self):
        self.driver.close()
        self.session.close()

    def allocatePatients(self, patients):
        """create a new patient node with initial data type
        :param attributes: dictionary of (name -> value) pairs for all attributes (must contain patient id as primary key)
        :return: none
        """
        with self.session.begin_transaction() as tx:
            for attributes in patients:
                # create the patient using the given ID
                tx.run("CREATE (n:Patient) "
                       "SET n = $attrs", attrs=attributes)
            tx.commit()

    def addAttributes(self, pat_id, attributes):
        """
        add attribute(s) to an existing patient node
        :param pat_id: patient id, primary key
        :param attributes: dictionary of (name -> value) pairs for all attributes
        :return: none
        """
        with self.session.begin_transaction() as tx:
            # find the patient using the given ID and add the attribute(s)
            tx.run("MATCH (n:Patient) WHERE n.Patient_ID={pid} "
                "SET n += $atts", pid=pat_id, atts=attributes)

    def updateAttribute(self, pat_id, att_name, val):
        """
        update the value of an existing attribute
        :param pat_id: patient id, primary key
        :param att_name: attribute label
        :param val: updated value for attribute
        :return: none
        """
        with self.session.begin_transaction() as tx:
            # create the attribute parameter
            att_param = {att_name: val}
            # find the patient using the given ID and update the attribute
            tx.run("MATCH (n:Patient) WHERE n.Patient_ID={pid} "
                "SET n += $att", pid=pat_id, att=att_param)

    def addRelation(self, from_id, to_id, measure):
        """
        create or update relation between two patient nodes in the db
        relations are 2-way relations
        :param from_id: patient node on one end of relations
        :param to_id: patient node on other end of relations
        :param measure: similarity or magnitude of relation
        :return: none
        """
        with self.session.begin_transaction() as tx:
            # find the patients to relate using the given IDs
            tx.run("MATCH (n:Patient), (m:Patient) "
                "WHERE n.Patient_ID={pid1} AND m.Patient_ID={pid2} "
                "CREATE (n)-[r:Similarity  { magnitude: {mag} }]->(m) "
                "RETURN r", pid1=from_id, pid2=to_id, mag=measure)

    def addRelationsFromBuffer(self, ids, buffer, name):
        """
        create relations in bulk
        :param buffer: iterable container of relation tuples <from, to, value>
        :return: none
        """
        with self.session.begin_transaction() as tx:
            # find the patients to relate using the given IDs
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    tx.run("MATCH (n:Patient), (m:Patient) "
                           "WHERE n.Patient_ID={pid1} AND m.Patient_ID={pid2} "
                           "CREATE (n)-[r:Similarity  { magnitude : {mag} }]->(m) "
                           "RETURN r", pid1=ids[i], pid2=ids[j], mag=buffer[i][j])
            tx.commit()


    def getPatient(self, pat_id):
        """
        return a single Patient node
        :param pat_id: patient id, primary key
        :return: single patient node as a bolt record
        """
        with self.session.begin_transaction() as tx:
            # find the patients to relate using the given IDs
            record = tx.run("MATCH (n:Patient) WHERE n.Patient_ID={pid} RETURN n", pid=pat_id).single()
            # return property list of single patient
            return record[0]

    def getPatientsRange(self, from_id, to_id):
        """
        return patient nodes in the range of record ID's
        :param from_id: first ID in range
        :param to_id: last ID in range
        :return: all nodes in range
        """
        with self.session.begin_transaction() as tx:
            # find the patients to relate using the given IDs
            records = tx.run("MATCH (n:Patient) "
                            "WHERE ID(n)>={id_1} AND ID(n)<={id_2} "
                            "RETURN n", id_1=from_id, id_2=to_id)
            # return all patients
            return list(records)

    def getSortedIDList(self):
        """
        get the list of all patients by record ID's in the database
        :return: list of strings (ID's)
        """
        with self.session.begin_transaction() as tx:
            # find the patients to relate using the given IDs
            results = tx.run("MATCH (n:Patient) RETURN ID(n) ORDER BY ID(n)").records()
            return list(results)

    def getPatientRelations(self, pat_id):
        """
        return all relations associated with a patient
        :param pat_id: patient's id, primary key
        :return: list of records of relations
        """
        with self.session.begin_transaction() as tx:
            # find the patients to relate using the given IDs
            results = tx.run("MATCH (n:Patient)-[r]-(m:Patient)"
                             " WHERE ID(n) = {id}"
                             " RETURN ID(m), r.magnitude ORDER BY ID(m)", id=pat_id).records()
            return list(results)

    def updateRelationsFromBuffer(self, ids, W):
        """
        update multiple existing relations
        :param ids: ids of nodes to update
        :param W: new values in matrix (upper triangular)
        :return: none
        """
        with self.session.begin_transaction() as tx:
            # find the patients to relate using the given IDs
            for i in range(len(ids)):
                for j in range(i+1, len(ids)):
                    tx.run("MATCH (n:Patient)-[r]-(m:Patient)"
                           " WHERE ID(n) = {pid1} AND ID(m) = {pid2}"
                           " SET r.magnitude = {value}"
                           " RETURN r", pid1=ids[i][0], pid2=ids[j][0], value=W[i][j])
                    # using j - 1 since each row in W excludes node i's relation to itself and is therefore always
                    # one index behind the id list
            tx.commit()
