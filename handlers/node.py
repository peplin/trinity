import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

class NodeHandler(BaseHandler):
    def post(self):
        id = self.get_json_argument('id')
        params = self.get_json_argument('node', {})

        with self.graph.transaction:  
            node = self.index[id]
            if not node:
                node = self.graph.node(**params)
                self.index[id] = node
        self.write({'id': id, 'node': params})
