#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options

from settings import settings
from handlers import RelationshipHandler, NodeHandler, StatHandler
import database

class Trinity(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/node", NodeHandler),
            (r"/node/([^/]+)/relationships", RelationshipHandler),
            (r"/node/([^/]+)/stats", StatHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = database.Connection(options.graph_path)


def main():
    app = Trinity()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
