import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

class RelationshipHandler(BaseHandler):
    def post(self, node_id):
        self.load_json()
        typ = self.get_argument('type')
        to = self.get_argument('to')
        data = self.get_argument('data', {})

        with self.graph.transaction:  
            node = self.find_node(node_id)
            to_node = self.find_node(to)
            getattr(node, typ)(to_node, **data)
