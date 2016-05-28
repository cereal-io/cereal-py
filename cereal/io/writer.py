import json

from collections import OrderedDict
from ..primitives import Avro
from ..primitives import Protobuf
from ..primitives import Thrift


class Writer(object):
    """Agnostic class used to generate standard output from any format.
    """
    def __init__(self, fmt):
        self._fmt = fmt
        self._formats = {
            'avro': {
                'fn': self._to_avro,
                'primitives': Avro,
            },
            'protobuf': {
                'fn': self._to_protobuf,
                'primitives': Protobuf,
            },
            'thrift': {
                'fn': self._to_thrift,
                'primitives': Thrift,
            },
        }

    def write(self, objects, indent, to=None, **kwargs):
        # Retrieve the private method based on the format type.
        self._primitives = getattr(
            self._formats[self._fmt]['primitives'],
            '_{to}'.format(to=to.upper())
        )
        fn = self._formats[to]['fn']
        return fn(objects, indent, **kwargs)

    def _to_avro(self, objects, indent, **kwargs):
        """Return serialized Avro records."""
        records = []
        for obj in objects:
            record = OrderedDict()
            record['type'] = 'record'
            record['name'] = obj.get('name') or obj.get('identifier')
            record['fields'] = []
            for field in obj['fields']:
                f = OrderedDict()
                t = field['type']
                try:
                    t = self._primitives[t]
                except KeyError:
                    continue
                f['type'] = t
                f['name'] = field['name']
                record['fields'].append(f)
            records.append(record)
        return json.dumps(records, indent=indent)

    def _to_protobuf(self, objects, indent, **kwargs):
        """Return serialized protocol buffers."""
        first = 0
        last = len(objects) - 1
        lines = ''
        for i, obj in enumerate(objects):
            lines += '\n' if i != first else ''
            # The `message` name can either be indexed via the `name`
            # key OR the `identifier` depending on the object type.
            message = obj.get('name') or obj.get('identifier')
            lines += 'message {} {{'.format(message)
            lines += '\n'
            fields = obj['fields']
            for j, field in enumerate(fields):
                identifier = field.get('identifier', j + 1)
                t = field['type']
                try:
                    t = self._primitives[t]
                except KeyError:
                    continue
                field['type'] = t
                lines += ' ' * indent + (
                    '{field[type]} {field[name]} = {identifier};'
                    .format(field=field, identifier=identifier)
                )
                lines += '\n'
            lines += '}\n' if i != last else '}'
        return lines

    def _to_thrift(self, objects, indent):
        """Return serialized Thrift messages."""
        first = 0
        last = len(objects) - 1
        lines = ''
        for i, obj in enumerate(objects):
            lines += '\n' if i != first else ''
            # The `message` name can either be indexed via the `name`
            # key OR the `identifier` depending on the object type.
            struct = obj.get('name') or obj.get('identifier')
            lines += 'struct {} {{'.format(struct)
            lines += '\n'
            fields = obj['fields']
            for j, field in enumerate(fields):
                identifier = field.get('identifier', j + 1)
                t = field['type']
                try:
                    t = self._primitives[t]
                except KeyError:
                    continue
                field['type'] = t
                lines += ' ' * indent + (
                    '{identifier}: {field[type]} {field[name]}'
                    .format(identifier=identifier, field=field)
                )
                lines += '\n'
            lines += '}\n' if i != last else '}'
        return lines
