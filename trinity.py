#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from handlers import RelationshipHandler, NodeHandler, StatHandler
import database

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
        settings = {'debug': True}
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = database.Connection(options.graph_path)


def main():
    tornado.options.parse_command_line()
    app = Trinity()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
