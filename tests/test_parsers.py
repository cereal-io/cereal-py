"""Tests for parser.py"""

import unittest
import json

from cereal import build


class ProtobufTestCase(unittest.TestCase):
    def setUp(self):
        self.svc = build('./examples/helloworld.proto')

    def test_to_avro(self):
        with open('./examples/helloworld.avsc') as fp:
            expected = json.loads(fp.read())
        actual = json.loads(self.svc.to_avro())
        self.assertEqual(actual, expected)


class AvroTestCase(unittest.TestCase):
    pass


class ThriftTestCase(unittest.TestCase):
    pass
