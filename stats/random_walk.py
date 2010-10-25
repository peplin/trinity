import neo4j
import random
from util import yapi


DEFAULT_DEPTH = 3 
NUM_WALKS = 1000
# Passed sorted list (desc order), return top nodes
TO_RETURN = lambda x: x
random.seed()


def random_walk(graph, node, depth=DEFAULT_DEPTH):
    if depth == 0:
        return [node]

    # Pick random neighbor
    neighbors = {}
    i = 0
    for r in node.relationships().outgoing:
        neighbors[(i, i + 1)] = r.getOtherNode(node)
        i += 1 
    if i == 0:
        # No neighbors
        return [node]
    r = random.randrange(i)
    for x,y in neighbors:
        if x <= r and r < y:
            return [node] + random_walk(graph, neighbors[(x,y)], depth-1)

def run(graph, index, node):
    nodes = {}
    for i in range(NUM_WALKS):
        with graph.transaction:
            walked_nodes = random_walk(graph, node)
        # Loop through nodes (that aren't the start node), count
        for n in filter(lambda m: m.id != node.id, walked_nodes):
            if nodes.has_key(n):
                nodes[n] += 1
            else:
                nodes[n] = 1

    # Have dict of nodes => count, weight each concept by freqency
    frequencies = {}
    for n in nodes:
        frequencies[n] = yapi(n['name'])

    max_frequency = 0
    for f in frequencies:
        if frequencies[f] > max_frequency:
            max_frequency = frequencies[f]
    max_count = 0
    for n in nodes:
        if nodes[n] > max_count:
            max_count = nodes[n]
    scaled_nodes = {}
    for f in frequencies:
        scaled_freq = float(frequencies[f]) / (float(max_frequency) / max_count)
        scaled_nodes[f] = float(nodes[f]) / scaled_freq

    return TO_RETURN([{'name': n['name'], 'count': scaled_nodes[n]}
            for n in sorted(scaled_nodes, key=scaled_nodes.__getitem__)])

