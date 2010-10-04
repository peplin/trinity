from nose.tools import ok_, eq_
from tornado.httpclient import HTTPRequest
import tornado.testing
from random import random
import json

import trinity

NODE_DATA = {'id': 'bueda', 'node': {'username': 'bueda', 'user_id': 12345}}
# LH #3 need a way to reset the graph after each test
NODE_DATA['id'] = int(random() * 1000000000)

class NodeHandlerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return trinity.Trinity()

    def setUp(self):
        super(NodeHandlerTest, self).setUp()
        self.data = NODE_DATA

    def test_create_node(self):
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node'),
                'POST',
                body=json.dumps(self.data)), self.stop)
        response = self.wait()
        eq_(response.code, 200)
