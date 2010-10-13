import tornado.testing

import trinity

class BaseTrinityTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return trinity.Trinity()

    def tearDown(self):
        self._app.shutdown()
