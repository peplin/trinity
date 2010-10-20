import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import simplejson
import datetime

from tornado import escape


class JPypeJSONEncoder(simplejson.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode JPype
    """
    def default(self, o):
        try:
            return super(JPypeJSONEncoder, self).default(o)
        except TypeError:
            try:
                if isinstance(o,dict):
                    return dict([ (k, super(JPypeJSONEncoder, self).default(v)) for k, v in data.iteritems() ])
                elif isinstance(o, (tuple, list, set)):
                    return [ super(JPypeJSONEncoder, self).default(v) for v in data ]
            #if it is a primitive of type int
            except TypeError:
                print type(o)
                return int(unicode(o))

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


    def _utf8(self,s):
        if isinstance(s, unicode):
            return s.encode("utf-8")
        assert isinstance(s, str)
        return s


    def write(self, chunk):
        # TODO override to handle JPype
        """Writes the given chunk to the output buffer.

        To write the output to the network, use the flush() method below.

        If the given chunk is a dictionary, we write it as JSON and set
        the Content-Type of the response to be text/javascript.

        Note that lists are not converted to JSON because of a potential
        cross-site security vulnerability.  All JSON output should be
        wrapped in a dictionary.  More details at
        http://haacked.com/archive/2008/11/20/anatomy-of-a-subtle-json-vulnerability.aspx
        """
        assert not self._finished
        if isinstance(chunk, dict):
            chunk = simplejson.dumps(chunk, cls=JPypeJSONEncoder, indent=4)
            #chunk = simplejson.dumps(chunk)
            #chunk = escape.json_encode(chunk)
            self.set_header("Content-Type", "text/javascript; charset=UTF-8")
        chunk = self._utf8(chunk)
        self._write_buffer.append(chunk)
        
