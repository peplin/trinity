import tornado.testing
from tornado.options import define, options

import trinity

class BaseTrinityTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        options.graph_path = '/tmp/neo4j-test'
        return trinity.Trinity()

    def tearDown(self):
        self._app.db.reset()
        self._app.db.shutdown()
