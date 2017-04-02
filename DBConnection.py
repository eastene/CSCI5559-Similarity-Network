# Evan Stene
# Class defining a connection to the graph db, and methods to add and update nodes in the network

from neo4j.v1 import GraphDatabase, basic_auth

class DBConnection:

  def __init__(self):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "dba"))
    self.session = driver.session()

  def __del__(self):
    self.session.close()

  def allocatePatient(self, pat_id):
    '''
    create a new, empty patient node
    :param pat_id: patient id, primary key
    :return: none
    '''
    with self.session.begin_transaction() as tx:
      # create the patient using the given ID
      tx.run("CREATE (n:Patient) "
             "SET n.id={pid}",{"pid": pat_id})
      tx.success = True

  def addAttributes(self, pat_id, attributes):
    '''
    add attribute(s) to an existing patient node
    :param pat_id: patient id, primary key
    :param attributes: dictionary of (name -> value) pairs for all attributes
    :return: none
    '''
    with self.session.begin_transaction() as tx:
      # find the patient using the given ID and add the attribute(s)
      tx.run("MATCH (n:Patient) WHERE n.id={pid} "
               "SET n = $atts", pid=pat_id, atts=attributes)

  def updateAttribute(self, pat_id, att_name, val):
    '''
    update the value of an existing attribute
    :param pat_id: patient id, primary key
    :param att_name: attribute label
    :param val: updated value for attribute
    :return: none
    '''
    with self.session.begin_transaction() as tx:
      # create the attribute parameter
      att_param = {att_name: val}
      # find the patient using the given ID and update the attribute
      tx.run("MATCH (n:Patient) WHERE n.id={pid} "
               "SET n = $att", pid=pat_id, att=att_param)

  def addRelation(self, from_id, to_id, measure):
    '''
    create or update relation between two patient nodes in the db
    relations are 2-way relations
    :param from_id: patient node on one end of relations
    :param to_id: patient node on other end of relations
    :param measure: similarity or magnitude of relation
    :return: none
    '''
    with self.session.begin_transaction() as tx:
      # find the patients to relate using the given IDs
      tx.run("MATCH (n:Patient, m:Patient) WHERE n.id={pid1} AND m.id={pid2}"
               "SET n-[r:Similarity magnitude:{mag}]-m", pid1=from_id, pid2=to_id, mag=measure)