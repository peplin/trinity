from nose.tools import ok_, eq_
from tornado.httpclient import HTTPRequest
import tornado.testing
import json

import trinity
from tests.test_node import NODE_DATA

class StatHandlerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return trinity.Trinity()

    def setUp(self):
        super(StatHandlerTest, self).setUp()
        self.http_client.fetch(HTTPRequest(
                self.get_url('/node'),
                'POST',
                body=json.dumps(NODE_DATA)), self.stop)

    def test_topics_stat(self):
        self.http_client.fetch(self.get_url(
                '/node/%s/stats?stat=%s' % (NODE_DATA['id'], 'topics')),
                self.stop)
        response = self.wait()
        eq_(response.code, 200)
