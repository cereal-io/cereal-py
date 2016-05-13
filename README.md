# Quickstart

The purpose of this module is to convert [Google Protocol Buffer](https://developers.google.com/protocol-buffers/) files to [Apache Avro](https://avro.apache.org/) files. The following example demonstrates how to use the parser:

    $ python parser.py -f helloworld.proto --out helloworld.avro

Given that the input file is `helloworld.proto`:

```protobuf
message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

The output will be `helloworld.avro`:

```json
[
    {
        "type": "record",
        "name": "HelloRequest",
        "fields": [
            {
                "type": "String",
                "name": "name"
            }
        ]
    },
    {
        "type": "record",
        "name": "HelloReply",
        "fields": [
            {
                "type": "String",
                "name": "message"
            }
        ]
    }
]
```
