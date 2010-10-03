import neo4j

class SubTopics(neo4j.Traversal):
    """Traverser that yields all subcategories of a category."""
    types = [neo4j.Incoming.is_a]
    returnable = neo4j.RETURN_ALL_BUT_START_NODE
    order = neo4j.BREADTH_FIRST
    stop = neo4j.STOP_AT_END_OF_GRAPH


class Topics(neo4j.Traversal):
    types = [
        neo4j.Outgoing.mentions_concept,
        neo4j.Outgoing.mentions,
        neo4j.Outgoing.is_a,

        ]
    order = neo4j.BREADTH_FIRST
    stop = neo4j.STOP_AT_END_OF_GRAPH
    def isReturnable(self, position):
        return not position.is_start and\
            position.last_relationship.type == 'is_a'

def run(graph, index, node):
    topics = {}
    for topic in Topics(node):
        topics[topic["name"]] = [sub["name"] for sub in SubTopics(topic)]
    return topics
