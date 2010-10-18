import neo4j
import random


DEFAULT_DEPTH = 5
NUM_WALKS = 100
# Passed sorted list (desc order), return top nodes
TO_RETURN = lambda x: x[:10]
random.seed()

def random_walk(graph, node, depth=DEFAULT_DEPTH):
    if depth == 0:
        return [node]

    # Pick random neighbor
    neighbors = {}
    i = 0
    for r in node.relationships().outgoing:
        neighbors[(i, i + int(r['count']))] = r.getOtherNode(node)
        i += int(r['count'])
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
    return TO_RETURN([{'name': n['name'], 'count': nodes[n]}
            for n in sorted(nodes, key=nodes.__getitem__)])

