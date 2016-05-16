# cereal-py [![Build Status](https://img.shields.io/travis/cereal-io/cereal-py/master.svg?style=flat-square)](https://travis-ci.org/cereal-io/cereal-py) ![GitHub tag](https://img.shields.io/github/tag/cereal-io/cereal-py.svg?style=flat-square&label=version) ![GitHub tag](https://img.shields.io/badge/style-pep8-7bcdea.svg?style=flat-square)

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
