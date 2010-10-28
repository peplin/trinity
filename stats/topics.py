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



#get the neighbours of the the node through 
def get_outgoing_neighbours_mentions(graph, index, node):
    neighbours = []
    with graph.transaction:
        for r in node.relationships('mentions_concept','mentions').outgoing:
                n = r.getOtherNode(node)
                if n != node:
                    neighbours.append((r,n))
    return neighbours

#get the neighbours of the the node through 
def get_outgoing_neighbours_type(graph, index, node):
    neighbours = []
    with graph.transaction:
        for r in node.relationships('is_a').outgoing:
                n = r.getOtherNode(node)
                if n != node:
                    neighbours.append((r,n))
    return neighbours

def get_outgoing_neighbours_likes(graph, index, node):
    neighbors = []
    with graph.transaction:
        for r in node.relationships('likes').outgoing:
            n = r.getOtherNode(node)
            if n != node:
                neighbors.append((r,n))
    return neighbors

def get_subtopic_types(graph, index, subtopic):
    types = get_outgoing_neighbours_type(graph, index, subtopic)
    typeDict = {}
    #for type in types:
    
def get_topics(graph, index, node):
    subtopics = get_outgoing_neighbours_mentions(graph, index, node)
    subtopics.extend(get_outgoing_neighbours_likes(graph, index, node))
    TD = {}
    for rs, subt in subtopics:
        topics =  get_outgoing_neighbours_type(graph, index, subt)
        rscount = 0
        try:
            rscount = rs["count"]
        except:
            rscount = 1
            
        for rt, t in topics:
            if t not in TD:
                TD[t] = {"count":rscount,
                         "subtopics":[{"name": subt["name"], 
                                       "info":{},
                                       "subtopics":{},
                                       "source" : [rs["text"]],
                                       "count": rscount}
                                     ],
                         "info":{},
                         "source": [rs["text"]],
                         "name": t["name"]
                         }
            elif t in TD:
                t_props = TD[t]
                t_props["count"] = t_props["count"] + rscount
                
                #if rs["text"] not in tprops["source"]:
                t_props["source"].append(rs["text"])
                
                t_props["subtopics"].append({"name": subt["name"], 
                                             "info":{},
                                             "subtopics":{},
                                             "source" : [rs["text"]],
                                             "count": rscount}) 
                
    topiclist = [TD[topic] for topic in TD.keys()]
    return topiclist
    

def run(graph, index, node):
    topics = get_topics(graph, index, node)           
    return topics
