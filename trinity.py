#!/usr/bin/env python

import neo4j
import json
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("graph_path", default="/var/neo4j/trinity",
        help="path to neo4j graph files")

class Trinity(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/node", NodeHandler),
            (r"/node/([^/]+)/relationships", RelationshipHandler),
            (r"/node/([^/]+)/stats", StatHandler),
        ]
        settings = {}
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the Neo4j graph across all handlers
        if not os.path.exists(os.path.dirname(options.graph_path)):
            raise RuntimeError("graph path %s doesn't exist"
                    % options.graph_path)
        self.graph = neo4j.GraphDatabase(options.graph_path)
        self.index = self.graph.index('objects', create=True)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def graph(self):
        return self.application.graph

    @property
    def index(self):
        return self.application.index

    def find_node(self, node_id):
        node = self.index[node_id]
        if not node:
            raise tornado.web.HTTPError(404, "node %s doesn't exist" % node_id)
        return node

    def load_json(self):
        self.request.arguments = json.loads(self.request.body)


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


class StatHandler(BaseHandler):
    def get(self, node_id):
        stat_module = self.get_argument('stat', None)
        node = self.find_node(node_id)

        # try to import stat from node states
        # run it!
        try:
            stat_method = __import__("stat.%s" % stat)
        except ImportError:
            raise tornado.web.HTTPError(400, "stat %s doesn't exist" % stat)

        results = stat_method(node)
        self.write(results)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Trinity())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
