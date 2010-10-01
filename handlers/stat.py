import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

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
