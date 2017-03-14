# CSCI 5559 Group 5
# Evan Stene - Lead

LOAD CSV WITH HEADERS FROM "file:/data1.csv" AS row
CREATE (n:Patient)
SET n = row;