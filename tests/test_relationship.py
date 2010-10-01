from nose.tools import ok_, eq_
from tornado.httpclient import HTTPRequest
import tornado.testing
import json

import trinity
from tests.test_node import NODE_DATA

RELATIONSHIP_DATA = {'to': 'bueda', 'data': {'other': 'data'},
        'type': 'MENTIONS'}

class RelationshipHandlerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return trinity.Trinity()

    def setUp(self):
        super(RelationshipHandlerTest, self).setUp()
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node'),
                'POST',
                body=json.dumps(NODE_DATA)), self.stop)
        self.data = RELATIONSHIP_DATA

    def test_create_relationship(self):
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node/%s/relationships' % NODE_DATA['id']),
                'POST',
                body=json.dumps(self.data)), self.stop)
        response = self.wait()
        eq_(response.code, 200)
