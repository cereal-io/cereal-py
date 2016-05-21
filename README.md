# cereal-py [![Build Status](https://img.shields.io/travis/cereal-io/cereal-py/master.svg?style=flat-square)](https://travis-ci.org/cereal-io/cereal-py) ![GitHub tag](https://img.shields.io/github/tag/cereal-io/cereal-py.svg?style=flat-square&label=version) ![Coveralls](https://img.shields.io/coveralls/cereal-io/cereal-py.svg?style=flat-square) ![GitHub tag](https://img.shields.io/badge/style-pep8-7bcdea.svg?style=flat-square)

The purpose of this module is to convert [Google Protocol Buffer](https://developers.google.com/protocol-buffers/) files, [Apache Avro](https://avro.apache.org/) files, and [Apache Thrift](https://thrift.apache.org/) files to their counterparts.

# Quickstart

The following example demonstrates how to convert a Google Protocol Buffer file to an Apache Avro file:

Given that the input file is `helloworld.proto`:

```protobuf
message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

```python
>>> from cereal import build
>>> svc = build('./examples/helloworld.proto')
>>> print(svc.to_avro())
[
    {
        "type": "record",
        "name": "HelloRequest",
        "fields": [
            {
                "type": "string",
                "name": "name"
            }
        ]
    },
    {
        "type": "record",
        "name": "HelloReply",
        "fields": [
            {
                "type": "string",
                "name": "message"
            }
        ]
    }
]
```

The `svc` object is an instance of the `Protobuf` class that contains a method called `.to_avro()`. This returns a serialized JSON string that serves as the contents for a `.avsc` file.

Converting a `.avsc` file to a `.proto` file uses a similar process:

```python
>>> from cereal import build
>>> svc = build('./examples/helloworld.avsc')
>>> print(svc.to_protobuf())
message HelloRequest {
    string name = 1;
}

message HelloReply {
    string message = 1;
}
```

# Protocol Buffers Enumerated Types

Given the following protocol buffer message:

```protobuf
// search.proto
message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
  enum Corpus {
    UNIVERSAL = 0;
    WEB = 1;
    IMAGES = 2;
    LOCAL = 3;
    NEWS = 4;
    PRODUCTS = 5;
    VIDEO = 6;
  }
  Corpus corpus = 4;
}
```

`cereal` converts enumerated types into the format defined in the [Avro specification](https://avro.apache.org/docs/current/spec.html#Enums):

```python
>>> from cereal import build
>>> svc = build('./examples/search.proto')
>>> print(svc.to_avro())
[
    {
        "type": "record",
        "name": "SearchRequest",
        "fields": [
            {
                "type": "string",
                "name": "query"
            },
            {
                "type": "int",
                "name": "page_number"
            },
            {
                "type": "int",
                "name": "result_per_page"
            },
            {
                "type": "enum",
                "name": "Corpus",
                "symbols": [
                    "UNIVERSAL",
                    "WEB",
                    "IMAGES",
                    "LOCAL",
                    "NEWS",
                    "PRODUCTS",
                    "VIDEO"
                ]
            }
        ]
    }
]
```
