import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

class NodeHandler(BaseHandler):
    def post(self):
        self.load_json()
        id = self.get_argument('id')
        params = self.get_argument('node', {})

        with self.graph.transaction:  
            node = self.index[id]
            if not node:
                node = self.graph.node(**params)
                self.index[id] = node
