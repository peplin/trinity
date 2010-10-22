import neo4j
import random
import operator


import commonware.log
logger = commonware.log.getLogger('trinity')



DEFAULT_DEPTH = 5
NUM_WALKS = 10000
random.seed()



def get_next_node(node):
    # get the count of relationships
    # select a random number
    # select the node
    count = 0
    neighbours=[]
    for r in node.relationships().outgoing:
        count += 1
        neighbours.append((r.type,r.getOtherNode(node)))

    if count == 0:
        return None
    else:
        rand_node_id = random.randrange(count)
        return neighbours[rand_node_id]


def random_walk(node, depth=DEFAULT_DEPTH):
    if depth == 0:
        return [node]
    
    path = []
    current_node = ("start",node)
    while 1:

        # select the node
        # and add it to the path        
        path.append(current_node)
        
        if len(path)>=depth:
            break
        current_node = get_next_node(current_node[1])
        
        if current_node[1] = "same_as"         
        if current_node is None:
            break   
    return path



def get_user_topics(node):
    logger.debug(u'getting topics for %s' % node)
    walk_count = 0
    P = {} # dictionary of predecessors
    C = {} # dictionary of counts
    
    for i in range(NUM_WALKS):
        if walk_count % 100 == 0:
            logger.debug(walk_count)
        walk_count += 1

        path = random_walk(node)
        if len(path) > 2:
            logger.debug("found one")
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
    return 1

def normalize_counts(user_counts):
    normalized = {}
    for k, v in user_counts.items():
        normalized[k] = user_counts[k] / get_normalized_count(k["name"])
    return normalized

def get_topics(graph, node):

    max_topics = 6
    topics = []

    with graph.transaction:
        user_counts, user_pred = get_user_topics(node)
        counts = normalize_counts(user_counts)
        sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
        if len(sorted_counts) < max_topics:
            max_topics = len(sorted_counts)
        
        for topic, count in sorted_counts[:max_topics]:            
            topics.append(get_subtopics_recursive(topic, user_pred, counts, node))
        
        
    graph.shutdown()
    return topics
    

def get_subtopics_recursive(topic, pred, counts, user):
    t= {}
    for k, v in topic.items():
        t[k] = v
    t["count"] = counts[topic]
    
    if topic not in pred:
        t["subtopics"] = []
    else:
        subtopics = []
        for sbtopic in pred[topic]:
            if user == sbtopic:
                continue
            else:
                subtopics.append(get_subtopics_recursive(sbtopic, pred, counts, user))
        t["subtopics"] = subtopics
        
    return t

def run(graph, index, node):
    return get_topics(graph, node)