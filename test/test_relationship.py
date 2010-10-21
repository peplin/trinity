from nose.tools import ok_, eq_
from tornado.httpclient import HTTPRequest
import json

from test.test_node import NODE_DATA
from test.base import BaseTrinityTest

ANOTHER_NODE_DATA = NODE_DATA.copy()
ANOTHER_NODE_DATA['id'] = 'peplin'

RELATIONSHIP_DATA = {'to': ANOTHER_NODE_DATA['id'], 'data': {'other': 'data',
        'count': 1}, 'link_type': 'MENTIONS'}

class RelationshipHandlerTest(BaseTrinityTest):
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
        data = json.loads(response.body)
        eq_(data['data']['other'], self.data['data']['other'])

    def test_append_relationship(self):
        self.data['append'] = True
        self.data['data']['new_data'] = 'bamf'
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node/%s/relationships' % NODE_DATA['id']),
                'POST',
                body=json.dumps(self.data)), self.stop)
        response = self.wait()
        eq_(response.code, 200)
        data = json.loads(response.body)
        eq_(data['data']['new_data'], self.data['data']['new_data'])

    def test_increment_attribute(self):
        self.data['increment'] = ['count']
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node/%s/relationships' % NODE_DATA['id']),
                'POST',
                body=json.dumps(self.data)), self.stop)
        response = self.wait()
        eq_(response.code, 200)
        data = json.loads(response.body)
        eq_(data['data']['count'], self.data['data']['count'] + 1)
