from nose.tools import ok_, eq_
from random import random
from tornado.httpclient import HTTPRequest
import tornado.testing
import json

import trinity
from tests.test_node import NODE_DATA

RELATIONSHIP_DATA = {'to': 'bueda', 'data': {'other': 'data'},
        'type': 'MENTIONS'}

ANOTHER_NODE_DATA = NODE_DATA
ANOTHER_NODE_DATA['id'] = "not_bueda"
# LH #3 need a way to reset the graph after each test
NODE_DATA['id'] = int(random() * 1000000000)
ANOTHER_NODE_DATA['id'] = int(random() * 1000000000)

class RelationshipHandlerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return trinity.Trinity()

    def setUp(self):
        super(RelationshipHandlerTest, self).setUp()

        self.http_client.fetch(HTTPRequest(
                self.get_url('/node'),
                'POST',
                body=json.dumps(NODE_DATA)), self.stop)
        self.wait()
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node'),
                'POST',
                body=json.dumps(ANOTHER_NODE_DATA)), self.stop)
        self.wait()
        self.data = RELATIONSHIP_DATA

    def test_create_relationship(self):
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node/%s/relationships' % NODE_DATA['id']),
                'POST',
                body=json.dumps(self.data)), self.stop)
        response = self.wait()
        eq_(response.code, 200)

