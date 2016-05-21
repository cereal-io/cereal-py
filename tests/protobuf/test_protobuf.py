"""Tests for protobuf parser."""

import json
import unittest

from cereal import build


class ProtobufTestCase(unittest.TestCase):
    def setUp(self):
        self.svc = build('./examples/helloworld.proto')

    def test_to_avro(self):
        with open('./examples/helloworld.avsc') as fp:
            expected = json.loads(fp.read())
        actual = json.loads(self.svc.to_avro())
        self.assertEqual(expected, actual)

    def test_syntax(self):
        syntax = self.svc.syntax
        self.assertEqual("proto3", syntax)

        temp_svc = build('./tests/protobuf/mocks/fail_test.proto')
        false_syntax = temp_svc.syntax
        self.assertEqual('proto2', false_syntax)
