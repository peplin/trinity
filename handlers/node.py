import neo4j
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

import logging
logger = logging.getLogger('trinity.' + __name__)


class NodeHandler(BaseHandler):
    @neo4j.transactional(BaseHandler.graph)
    def post(self):
        node_id = unicode(self.get_json_argument('id')).lower()
        params = self.get_json_argument('node', {})

        node = self.index[node_id]
        if not node:
            node = self.graph.node(**params)
            self.index[node_id] = node
            logger.debug("Created node %s with ID %s and data %s"
                    % (node, node_id, params))
        logger.debug("Found existing node %s with ID %s -- not creating another"
                % (node, node_id))
        self.write({'id': node_id, 'node': params})
