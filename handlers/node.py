import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

class NodeHandler(BaseHandler):
    def post(self):
        self.load_json()
        id = self.get_argument('id')
        # Can't use get_argument here, as it clobbers a nested dictionary
        params = self.request.arguments.get('node', {})

        with self.graph.transaction:  
            node = self.index[id]
            if not node:
                node = self.graph.node(**params)
                self.index[id] = node
