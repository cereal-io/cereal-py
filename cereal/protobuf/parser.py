import json
import re

from collections import OrderedDict
from ..meta import ProtocolMeta


class Protobuf(ProtocolMeta):
    # To Avro
    PRIMITIVES = {
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

    def __init__(self, filepath):
        super(Protobuf, self).__init__(filepath)
        with open(self._filepath) as fp:
            match = re.search(self._patterns['syntax'], fp.read())
        if match is not None:
            syntax = match.group('syntax')
        else:
            syntax = 'proto2'
        self._syntax = syntax

    @property
    def syntax(self):
        return self._syntax

    def to_avro(self, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Avro file."""
        schemas = []
        with open(self._filepath) as fp:
            lines = fp.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            match = re.match(self._patterns['message'], line)
            if match is None:
                continue
            record = OrderedDict()
            record['type'] = 'record'
            # Google Protocol Buffer message name.
            record['name'] = match.group('name')
            record['fields'] = []
            j = i
            while True:
                # Increment `j` by 1 to ignore the `message` line
                # itself.
                j += 1
                line = lines[j].strip()
                if line.endswith('}'):
                    break
                if line == '':
                    continue
                match = re.match(self._patterns['field'], line)
                if match is None:
                    continue
                rule, t, identifier, _ = match.groups()
                try:
                    t = self.PRIMITIVES[t]
                except KeyError:
                    continue
                record['fields'].append({
                    'name': identifier,
                    'type': t,
                })
            schemas.append(record)
        return json.dumps(schemas, indent=indent)
