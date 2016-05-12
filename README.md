    $ python parser.py -f helloworld.proto --out helloworld.avro

**helloworld.proto**

```protobuf
message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

**helloworld.avro**

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
