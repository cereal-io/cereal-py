"""Tests for various parsers."""

import unittest
import json

from cereal import build


class ProtobufTestCase(unittest.TestCase):
    def setUp(self):
        self.svc = build('./examples/helloworld.proto')

    def test_to_avro(self):
        with open('./examples/helloworld.avsc') as fp:
            expected = json.loads(fp.read())
        actual = self.svc.to_avro()
        self.assertEqual(actual, expected)


class AvroTestCase(unittest.TestCase):
    def setUp(self):
        self.svc = build('./examples/helloworld.avsc')

    def test_to_protobuf(self):
        expected = """
message HelloRequest {
    string name = 1;
}

message HelloReply {
    string message = 1;
}
        """
        expected = expected.strip()
        actual = self.svc.to_protobuf(serialized=True)
        self.assertEqual(expected, actual)


class ThriftTestCase(unittest.TestCase):
    pass
