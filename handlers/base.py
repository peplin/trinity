import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

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
        if not node:
            raise tornado.web.HTTPError(404, "node %s doesn't exist" % node_id)
        return node

    def load_json(self):
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            raise tornado.web.HTTPError(400, "Could not decode JSON: %s"
                    % self.request.body)

    def get_json_argument(self, name,
            default=tornado.web.RequestHandler._ARG_DEFAULT, strip=True):
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                raise tornado.web.HTTPError(400, "Missing argument %s" % name)
            return default
        arg = self.request.arguments[name]
        return arg

    def write(self):
        # TODO override to handle JPype
        
