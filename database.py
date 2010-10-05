import neo4j
import os.path

class Connection(object):
    def __init__(self, path):
        # Have one global connection to the Neo4j graph across all handlers
        if not os.path.exists(os.path.dirname(path)):
            raise RuntimeError("graph path %s doesn't exist" % path)
        self.path = path
        self.reconnect()

    def __del__(self):
        # LH #3 - this isn't being called
        self.shutdown()

    def shutdown(self):
        """Closes this database connection."""
        if getattr(self, "_graph", None) is not None:
            self.graph.shutdown()
            self.graph = None
            self.index = None

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.shutdown()
        self.graph = neo4j.GraphDatabase(self.path)
        self.index = self.graph.index('objects', create=True)
