import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import logging
logger = logging.getLogger('trinity.' + __name__)


class NodeNotFoundError(Exception): pass


class JPypeJSONEncoder(json.JSONEncoder):
    """JSONEncoder subclass that knows how to encode JPype. """
    def default(self, data):
        if 'jpype' in unicode(data.__class__):
            value = unicode(data)
            try:
                value = int(value)
            except TypeError:
                pass
            except ValueError:
                pass
            return value
        return


class BaseHandler(tornado.web.RequestHandler):
    @property
    def graph(self):
        return self.application.db.graph

    @property
    def index(self):
        return self.application.db.index

    def find_node(self, node_id):
        if isinstance(node_id, basestring):
            node_id = node_id.lower()
        node = self.index[node_id]
        if node is None:
            msg = "Node with ID '%s' doesn't exist" % node_id
            logger.debug(msg)
            raise NodeNotFoundError(msg)
        logger.debug("Found node %s with ID '%s'" % (node, node_id))
        return node

    def find_node_or_404(self, node_id):
        try:
            return self.find_node(node_id)
        except NodeNotFoundError, error:
            raise tornado.web.HTTPError(404, str(error))

    def load_json(self):
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def write(self, chunk):
        """If chunk is a dict, writes out to JSON using custom serializer than
        handlers JPype objects.
        """
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk, cls=JPypeJSONEncoder)
            self.set_header("Content-Type", "text/javascript; charset=UTF-8")
        super(BaseHandler, self).write(chunk)
