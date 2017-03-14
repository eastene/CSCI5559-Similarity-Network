LOAD CSV WITH HEADERS FROM "file:/data1.csv" AS row
CREATE (n:Patient)
SET n = row;