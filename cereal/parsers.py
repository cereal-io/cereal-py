import json
import re

from collections import OrderedDict
from meta import ProtocolMeta


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
        prog = re.compile(r'syntax\s=\s\"(proto\d+)\";')
        with open(self._filepath) as fp:
            match = prog.search(fp.read())
        if match is not None:
            syntax = match.group(1)
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
        prog = re.compile(r'^message\s(\w+)\s\{$')
        for i in range(len(lines)):
            line = lines[i].strip()
            match = prog.match(line)
            if match is None:
                continue
            record = OrderedDict()
            record['type'] = 'record'
            # Google Protocol Buffer message name.
            record['name'] = match.group(1)
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
                field = line.split()
                t, identifier = field[:2]
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


class Avro(ProtocolMeta):
    # To protobuf
    PRIMITIVES = {
        'null': None,
        'boolean': 'bool',
        'int': 'sint32',
        'long': 'sint64',
        'float': 'float',
        'double': 'double',
        'bytes': 'bytes',
        'string': 'string',
    }

    def __init__(self, filepath):
        super(Avro, self).__init__(filepath)

    def to_protobuf(self, indent=4):
        lines = ''
        with open(self._filepath) as fp:
            records = json.loads(fp.read())
        first = 0
        last = len(records) - 1
        for i in range(len(records)):
            lines += '\n' if i != first else ''
            lines += 'message {}'.format(records[i]['name'])
            lines += ' {\n'
            fields = records[i]['fields']
            for j in range(len(fields)):
                lines += ' ' * indent + '{} {} = {};\n'.format(
                    self.PRIMITIVES[fields[j]['type']],
                    fields[j]['name'],
                    j + 1,
                )
            lines += '}' if i == last else '}\n'
        return lines
