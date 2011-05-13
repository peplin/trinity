from nose.tools import ok_, eq_
from tornado.httpclient import HTTPRequest
import json

from tests.base import BaseTrinityTest

NODE_DATA = {'id': 'bueda', 'node': {'username': 'bueda', 'user_id': 12345}}

class NodeHandlerTest(BaseTrinityTest):
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
