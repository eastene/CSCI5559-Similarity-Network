# CSCI 5559 Group 5
# Evan Stene - Lead

# currently this returns a graph database with ~600 nodes, each with ~600 attributes
# need to convert those attributes to edges
LOAD CSV WITH HEADERS FROM "file:/data1.csv" AS row
CREATE (n:Patient)
SET n = row;