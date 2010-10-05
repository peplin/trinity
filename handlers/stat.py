import neo4j
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import importlib
from handlers.base import BaseHandler

class StatHandler(BaseHandler):
    @neo4j.transactional(BaseHandler.graph)
    def get(self, node_id):
        name = self.get_argument('stat', None)
        node = self.find_node(node_id)

        try:
            module = importlib.import_module("stats.%s" % name)
        except ImportError:
            raise tornado.web.HTTPError(400,
                    "stat %s doesn't exist" % name)
        results = getattr(module, 'run')(self.graph, self.index, node)
        self.write({'results': results})
