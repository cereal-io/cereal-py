class Avro(object):
    _PROTOBUF = {
        'null': None,
        'boolean': 'bool',
        'int': 'sint32',
        'long': 'sint64',
        'float': 'float',
        'double': 'double',
        'bytes': 'bytes',
        'string': 'string',
    }

    _THRIFT = {
        'null': None,
        'boolean': 'bool',
        'int': 'i32',
        'long': 'i64',
        'float': 'double',
        'double': 'double',
        'bytes': 'binary',
        'string': 'string',
    }


class Protobuf(object):
    _AVRO = {
        'double': 'double',
        'float': 'float',
        'int32': 'int',
        'int64': 'long',
        'uint32': 'int',
        'uint64': 'long',
        'sint32': 'int',
        'sint64': 'long',
        'fixed32': 'int',
        'fixed64': 'long',
        'sfixed32': 'int',
        'sfixed64': 'long',
        'bool': 'boolean',
        'string': 'string',
        'bytes': 'bytes',
    }

    _THRIFT = {
        'double': 'double',
        'float': 'double',
        'int32': 'i32',
        'int64': 'i64',
        'uint32': 'i32',
        'uint64': 'i64',
        'sint32': 'i32',
        'sint64': 'i64',
        'fixed32': 'i32',
        'fixed64': 'i64',
        'sfixed32': 'i32',
        'sfixed64': 'i64',
        'bool': 'bool',
        'string': 'string',
        'bytes': 'binary',
    }


class Thrift(object):
    _AVRO = {
        'bool': 'bool',
        'byte': 'int',
        'i32': 'int',
        'i64': 'long',
        'double': 'double',
        'string': 'string',
        'binary': 'bytes',
    }

    _PROTOBUF = {
        'bool': 'bool',
        'byte': 'fixed64',
        'i32': 'int32',
        'i64': 'int64',
        'double': 'double',
        'string': 'string',
        'binary': 'bytes',
    }
