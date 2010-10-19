import neo4j
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

class NodeHandler(BaseHandler):
    @neo4j.transactional(BaseHandler.graph)
    def post(self):
        node_id = unicode(self.get_json_argument('id'))
        if isinstance(node_id, basestring):
            node_id = node_id.lower()
        params = self.get_json_argument('node', {})

        node = self.index[node_id]
        if not node:
            node = self.graph.node(**params)
            self.index[node_id] = node
        self.write({'id': node_id, 'node': params})
