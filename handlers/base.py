import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

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

    def get_json_argument(self, name,
            default=tornado.web.RequestHandler._ARG_DEFAULT, strip=True):
        if not self.request.arguments:
            self.load_json()
        arg = self.request.arguments[name]
        if not arg:
            if default is self._ARG_DEFAULT:
                raise HTTPError(404, "Missing argument %s" % name)
            return default
        return arg
