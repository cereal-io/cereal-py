"""Tests for various parsers."""

import unittest

from cereal import build
from cereal.models import Message
from cereal.models import Field


class ProtobufTestCase(unittest.TestCase):
    def setUp(self):
        self.svc = build('./examples/helloworld.proto')

    def test_to_serialized_avro(self):
        with open('./examples/helloworld.avsc') as fp:
            expected = fp.read().strip()
        actual = self.svc.to_avro(serialized=True)
        self.assertEqual(actual, expected)


class AvroTestCase(unittest.TestCase):
    def setUp(self):
        self.svc = build('./examples/helloworld.avsc')

    def test_to_serialized_protobuf(self):
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
        self.assertEqual(actual, expected)

    def test_to_deserialized_protobuf(self):
        import pdb
        pdb.set_trace()
        expected = [
            Message(name='HelloRequest', fields=[
                Field(type_='string', name='name')
            ]),
            Message(name='HelloReply', fields=[
                Field(type_='string', name='message')
            ]),
        ]
        actual = self.svc.to_protobuf()
        self.assertEqual(actual, expected)


class ThriftTestCase(unittest.TestCase):
    pass
