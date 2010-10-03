import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import importlib
from handlers.base import BaseHandler

class StatHandler(BaseHandler):
    def get(self, node_id):
        name = self.get_argument('stat', None)
        with self.graph.transaction:  
            node = self.find_node(node_id)

            # try to import stat from node states
            # run it!
            try:
                module = importlib.import_module("stats.%s" % name)
            except ImportError:
                raise tornado.web.HTTPError(400,
                        "stat %s doesn't exist" % name)
            # TODO can we do this async?
            results = getattr(module, 'run')(self.graph, self.index, node)
        self.write({'results': results})
