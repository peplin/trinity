#!/usr/bin/env python
import unittest

TEST_MODULES = [
    'test.test_node',
    'test.test_stat',
    'test.test_relationship',
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
    import tornado.testing
    tornado.testing.main()
