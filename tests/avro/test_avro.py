"""Tests for Avro parser."""

import json
import unittest

from cereal import build


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
        actual = self.svc.to_protobuf(syntax='proto2')
        self.assertEqual(expected, actual)

    def test_to_protobuf_with_enumerated_types(self):
        svc = build('./tests/mocks/search.proto')
        expected = [
            {
                'type': 'record',
                'name': 'SearchRequest',
                'fields': [
                    {
                        'type': 'string',
                        'name': 'query'
                    },
                    {
                        'type': 'int',
                        'name': 'page_number'
                    },
                    {
                        'type': 'int',
                        'name': 'result_per_page'
                    },
                    {
                        'type': 'enum',
                        'name': 'Corpus',
                        'symbols': [
                            'UNIVERSAL',
                            'WEB',
                            'IMAGES',
                            'LOCAL',
                            'NEWS',
                            'PRODUCTS',
                            'VIDEO'
                        ]
                    }
                ]
            }
        ]
        actual = json.loads(svc.to_avro())
        self.assertEqual(expected, actual)
