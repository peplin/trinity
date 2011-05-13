import neo4j
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import importlib
from handlers.base import BaseHandler

import logging
logger = logging.getLogger('trinity.' + __name__)


class StatHandler(BaseHandler):
    @neo4j.transactional(BaseHandler.graph)
    def get(self, node_id):
        name = self.get_argument('stat', None)
        node = self.find_node_or_404(node_id)

        try:
            module = importlib.import_module("stats.%s" % name)
        except ImportError:
            msg = "Statistic %s doesn't exist (or couldn't import)" % name
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)
        results = getattr(module, 'run')(self.graph, self.index, node)
        logger.debug("Calculated statistic %s for node %s to be %s"
                % (module, node, results))
        self.write({'results': results})
