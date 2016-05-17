import json
import re

from ..meta import ProtocolMeta


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

    def to_protobuf(self, indent=4, syntax='proto3'):
        lines = ''
        with open(self._filepath) as fp:
            records = json.loads(fp.read())
        match = re.match(r'^proto(\d+)$', syntax)
        if match:
            syntax = match.group(1)
            # If protocol buffers syntax is greater than or equal to v3,
            # then include the `syntax` statement at the beginning of
            # the file.
            if int(syntax) >= 3:
                lines += 'syntax = "proto{}";\n'.format(syntax)
                lines += '\n'
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
            lines += '}\n' if i != last else '}'
        return lines
