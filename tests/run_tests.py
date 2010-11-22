#!/usr/bin/env python
import unittest

TEST_MODULES = [
    'tests.test_node',
    'tests.test_stat',
    'tests.test_relationship',
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
    import tornado.testing
    tornado.testing.main()
