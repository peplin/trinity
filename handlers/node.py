import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

class NodeHandler(BaseHandler):
    def post(self):
        node_id = self.get_json_argument('id').lower()
        params = self.get_json_argument('node', {})

        with self.graph.transaction:  
            node = self.index[node_id]
            if not node:
                node = self.graph.node(**params)
                self.index[node_id] = node
        self.write({'id': node_id, 'node': params})
