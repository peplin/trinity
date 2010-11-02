import neo4j
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler, NodeNotFoundError

import logging
logger = logging.getLogger('trinity.' + __name__)


class NodeHandler(BaseHandler):
    @neo4j.transactional(BaseHandler.graph)
    def post(self):
        node_id = unicode(self.get_json_argument('id')).lower()
        params = self.get_json_argument('node', {})

        try:
            node = self.find_node(node_id)
        except NodeNotFoundError:
            node = self.graph.node(**params)
            self.index[node_id] = node
            logger.debug("Created node %s with 'ID' %s and data %s"
                    % (node, node_id, params))
        else:
            logger.debug("Found existing node %s with ID %s -- "
                    "not creating another" % (node, node_id))
        self.write({'id': node_id, 'node': params})
