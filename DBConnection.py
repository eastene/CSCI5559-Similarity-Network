from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "dba"))
session = driver.session()


def allocatePatient(pat_id):
  '''
  
  :param pat_id: patient id, primary key
  :return: none
  '''
  with session.begin_transaction() as tx:
    # create the patient using the given ID
    tx.run("CREATE (n:Patient) "
           "SET n.id={pid}",{"pid": pat_id})
    tx.success = True

def addAttributes(pat_id, attributes):
  '''
  
  :param pat_id: patient id, primary key
  :param attributes: dictionary of (name -> value) pairs for all attributes
  :return: none
  '''
  with session.begin_transaction() as tx:
    # find the patient using the given ID
    for attr in attributes:
      tx.run("MATCH (n:Patient) WHERE n.id={pid} "
             "SET n = $atts", pid=pat_id, atts=attributes)

# quick testing 
allocatePatient(1)
addAttributes(1, {'name':'bob','age':23})
session.close()
