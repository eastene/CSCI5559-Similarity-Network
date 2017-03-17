/**
 * Created by Evan Stene on 3/17/17.
 */

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Label;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.index.Index;
import org.neo4j.graphdb.index.IndexManager;
import org.neo4j.logging.Log;
import org.neo4j.procedure.Context;
import org.neo4j.procedure.Name;
import org.neo4j.procedure.PerformsWrites;
import org.neo4j.procedure.Procedure;

import org.neo4j.procedure.*;

public class Creator {

    @Context
    public GraphDatabaseService db;

    @Procedure( name = "snf.create_from_csv", mode = Mode.WRITE )
    public void create(String filename){
        //TODO fill out this method
    }
}
