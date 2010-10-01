#!/usr/bin/env python

import neo4j
import json
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from handlers import RelationshipHandler, NodeHandler, StatHandler

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


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Trinity())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
