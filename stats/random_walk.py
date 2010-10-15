import neo4j
import random

from logbook import Logger
log = Logger('trinity.topics')


DEFAULT_DEPTH = 5
NUM_WALKS = 100
# Passed sorted list (desc order), return top nodes
TO_RETURN = lambda x: x[:10]
random.seed()

def random_walk(graph, node, depth=DEFAULT_DEPTH):
    # Pick random neighbor
    neighbors = {}
    i = 0
    for r in node.relationships().outgoing:
        #TODO replace with i + r['count']
        neighbors[(i, i + 1)] = r.getOtherNode(node)
        i += 1
    choice = random.range(i)
    for x,y in neighbors:
        if x <= i and i < y:
            return [node].extend(random_walk(graph, neighbors[(x,y)], depth-1))

def run(graph, index, node):
    nodes = {}
    for i in range(NUM_WALKS):
        with graph.transaction:
            walked_nodes = random_walk(graph, node)
        # Loop through nodes (that aren't the start node), count
        for n in filter(lambda m: m.id != node.id, walked_nodes):
            if nodes.has_key(n):
                nodes[n]++
            else
                nodes[n] = 1
    return TO_RETURN(sorted(nodes, key=nodes.__getitem__))                

