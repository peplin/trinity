import neo4j
import random
import operator
import networkx as nx
from util import yapi
from collections import deque

import logging
logger = logging.getLogger(__name__)

#TODO requires same-as links to function well. Should work anyway

DEFAULT_DEPTH = 5
NUM_WALKS = 10000
random.seed()

def get_dict(node):
    d = {}
    for k in node:
        if k in ['source', 'name', 'relevancy', 'subtopics']:
            d[k] = node[k]
    return d

def get_nx_graph(graph, start, maxpath=6):
    D = {}
    ID = {}
    maps = {}
    nxgraph = nx.MultiDiGraph()
    queue = deque()
    
    ID[start.id] = 0
    
    ndict = get_dict(start)
    nxgraph.add_node(start.id, **ndict)
    maps[start.id] = start
    queue.append(start.id)
    
    while len(queue)>0:
        v = queue.popleft()
        currentNode = maps[v]
        D[v] = ID[v]
        
        if D[v] > maxpath:
            break
        for r in currentNode.relationships().outgoing:
            current_dict = get_dict(currentNode)
            if r.type == 'same_as':
                sameNode = r.getOtherNode(currentNode)
                current_dict.update(get_dict(sameNode))
                
                for r1 in sameNode.relationships().outgoing:
                    endNode = r1.getOtherNode(sameNode)
                    end_node_props = get_dict(endNode)
                    nxgraph.add_node(endNode.id, **end_node_props)
                    vw1length = D[v] + 1
                    ID[endNode.id] = vw1length 
                    maps[endNode.id] = endNode
                    nxgraph.add_edge(v, endNode.id, type=r1.type)
                    queue.append(endNode.id)
            if r.type == 'twitter':
                sameNode = r.getOtherNode(currentNode)
                current_dict.update(get_dict(sameNode))
                
                for r1 in sameNode.relationships().outgoing:
                    endNode = r1.getOtherNode(sameNode)
                    end_node_props = get_dict(endNode)
                    nxgraph.add_node(endNode.id, **end_node_props)
                    vw1length = D[v] + 1
                    ID[endNode.id] = vw1length 
                    maps[endNode.id] = endNode
                    nxgraph.add_edge(v, endNode.id, type=r1.type)
                    queue.append(endNode.id)
            if r.type == 'facebook':
                sameNode = r.getOtherNode(currentNode)
                nd2 = get_dict(sameNode) 
                for r1 in sameNode.relationships().outgoing:
                    endNode = r1.getOtherNode(sameNode)
                    end_node_props = get_dict(endNode)
                    nxgraph.add_node(endNode.id, **end_node_props)
                    vw1length = D[v] + 1
                    ID[endNode.id] = vw1length 
                    maps[endNode.id] = endNode
                    nxgraph.add_edge(v, endNode.id, type=r1.type)
                    queue.append(endNode.id)
            elif r == 'mentions':
                continue
            else:
                endNode = r.getOtherNode(currentNode)
                nd2 = get_dict(endNode) 
                maps[endNode.id] = endNode
                #add the edge to the nx graph
                vwLength = D[v] + 1
                nxgraph.add_node(endNode.id, **nd2)
                ID[endNode.id] = vwLength
                nxgraph.add_edge(v, endNode.id, type=r.type)
                queue.append(endNode.id)
            
    return nxgraph

def get_next_node(graph, nodeid):
    outd = graph.out_degree(nodeid)

    if outd == 0:
        return None
    else:
        rand_edge = random.randrange(graph.out_degree(nodeid))
        edge = graph.out_edges(nodeid,data=True)[rand_edge]
        return (edge[2]["type"], edge[1])

def random_walk(graph, nodeid, depth=DEFAULT_DEPTH):
    if depth == 0:
        return [nodeid]    
    path = []
    current_node = ("start",nodeid)
    while 1:
        # select the node and add it to the path
        path.append(current_node)
        if len(path) >= depth:
            break

        current_node = get_next_node(graph, current_node[1])
        if current_node is None:
            break

    return path

def get_user_topics(graph, node):
    logger.debug(u'getting topics for %s' % node)
    P = {} # dictionary of predecessors
    C = {} # dictionary of counts
    
    for i in range(NUM_WALKS):
        path = random_walk(graph, node)
        previous_node = node            
        for r, n in path[1:]:
            # add the predecessors
            if n in P:
                if previous_node not in P[n]:
                    P[n].append(previous_node)
            else:
                P[n] = [previous_node]
                                 
            # add the counts
            if n in C:
                C[n] += 1
            else:
                C[n] = 1      
            previous_node = n
            
    return (C, P)

def get_normalized_count(name):
    norm_count = yapi(name)
    #norm_count = 1
    return norm_count

def normalize_counts(graph, user_counts):
    normalized = {}
    for k, v in user_counts.items():
        name = graph.node[k]["name"]
        normalized[k] = user_counts[k] / get_normalized_count(name)
    return normalized

def get_topics(graph, node):
    max_topics = 6
    topics = []
    
    nxgraph = None
    nodeid = node.id
    
    logger.debug(u'executing networkx graph transformation')
    with graph.transaction:
        nxgraph = get_nx_graph(graph, node, maxpath=max_topics)

    if nxgraph:
        user_counts, user_pred = get_user_topics(nxgraph, nodeid)
        logger.debug(u'normalizing counts')
        counts = normalize_counts(nxgraph, user_counts)
        sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
        if len(sorted_counts) < max_topics:
            max_topics = len(sorted_counts)

        logger.debug(u'generating subtopics')
        for topic, count in sorted_counts[:max_topics]:            
            topics.append(get_subtopics_recursive(nxgraph, topic, user_pred, counts, nodeid))
            
            
        return topics
    else:
        return None
    
def get_subtopics_recursive(graph, topic, pred, counts, user):
    t= {}    
    for k, v in graph.node[topic].items():
        t[k] = v
    t["relevancy"] = counts[topic]
    
    if topic not in pred:
        t["subtopics"] = []
    else:
        subtopics = []
        for sbtopic in pred[topic]:
            if user == sbtopic:
                continue
            else:
                subtopics.append(get_subtopics_recursive(graph, sbtopic, pred, counts, user))
        t["subtopics"] = subtopics
        
    return t

def run(graph, index, node):
    return get_topics(graph, node)
