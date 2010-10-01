from tornado.httpclient import HTTPRequest
import tornado.testing
import json

import trinity

class NodeHandlerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return trinity.Trinity()

    def setUp(self):
        super(NodeHandlerTest, self).setUp()
        self.data = {}

    def test_foo(self):
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node'),
                'POST',
                body=json.dumps(self.data)), self.stop())
        response = self.wait()
