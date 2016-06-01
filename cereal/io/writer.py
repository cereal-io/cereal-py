import json

from collections import OrderedDict
from ..mappings import Avro
from ..mappings import Protobuf
from ..mappings import Thrift
from ..models import Enumeration


class Writer(object):
    """Agnostic class used to generate standard output from any format.
    """
    def __init__(self, fmt):
        self._fmt = fmt
        self._formats = {
            'avro': {
                'fn': self._to_avro,
                'mappings': Avro,
            },
            'protobuf': {
                'fn': self._to_protobuf,
                'mappings': Protobuf,
            },
            'thrift': {
                'fn': self._to_thrift,
                'mappings': Thrift,
            },
        }

    def write(self, objects, indent, to=None, **kwargs):
        # Retrieve the private method based on the format type.
        self._mappings = getattr(
            self._formats[self._fmt]['mappings'],
            '_{to}'.format(to=to.name)
        )
        fn = self._formats[to.name.lower()]['fn']
        return fn(objects, indent, **kwargs)

    def _to_avro(self, objects, indent, **kwargs):
        """Return serialized Avro records."""
        records = []
        for obj in objects:
            record = OrderedDict()
            record['type'] = 'record'
            record['name'] = obj.name
            record['fields'] = []
            fields = obj.fields
            for i, _ in enumerate(fields):
                field = OrderedDict()
                type_ = fields[i].type_
                try:
                    # If the type of the field does not exist, continue
                    # to the next field.
                    type_ = self._mappings[type_]
                except KeyError:
                    # Primitive type could not be determined, check if
                    # the type is an enumeration or of another type.
                    if isinstance(fields[i], Enumeration):
                        field['type'] = fields[i].type_
                        field['name'] = fields[i].name
                        field['symbols'] = fields[i].symbols
                field['type'] = type_
                field['name'] = fields[i].name
                record['fields'].append(field)
            records.append(record)
        return json.dumps(records, indent=indent, separators=(',', ': '))

    def _to_protobuf(self, objects, indent, **kwargs):
        """Return serialized protocol buffers."""
        first = 0
        lines = ''
        for i, obj in enumerate(objects):
            lines += '\n' if i != first else ''
            message = obj.name
            lines += 'message {} {{\n'.format(message)
            fields = obj.fields
            for j, field in enumerate(fields):
                field.identifier = field.identifier or j + 1
                type_ = field.type_
                try:
                    # If the type of the field does not exist, continue
                    # to the next field.
                    type_ = self._mappings[type_]
                    field.type_ = type_
                except KeyError:
                    if isinstance(field, Enumeration):
                        lines += (
                            ' ' * indent + '{} {} {{'
                            .format(field.type_, field.name)
                        )
                        lines += '\n'
                        for i, symbol in enumerate(field.symbols):
                            lines += (
                                ' ' * (indent * 2) + '{} = {};\n'
                                .format(symbol, i + 1)
                            )
                        lines += ' ' * indent + '}\n'
                        # Reassign the `type_` attribute to the field
                        # `name` and reassign the field `name` to be
                        # lowercased.
                        field.type_ = field.name
                        field.name = field.name.lower()
                lines += ' ' * indent + (
                    '{field.type_} {field.name} = {field.identifier};'
                    .format(field=field)
                )
                lines += '\n'
            lines += '}\n'
        lines = lines.strip()
        return lines

    def _to_thrift(self, objects, indent):
        """Return serialized Thrift messages."""
        first = 0
        lines = ''
        for i, obj in enumerate(objects):
            lines += '\n' if i != first else ''
            struct = obj.name
            lines += 'struct {} {{\n'.format(struct)
            fields = obj.fields
            for j, field in enumerate(fields):
                identifier = field.identifier or j + 1
                type_ = field.type_
                try:
                    # If the type of the field does not exist, continue
                    # to the next field.
                    type_ = self._mappings[type_]
                except KeyError:
                    continue
                field.type_ = type_
                lines += ' ' * indent + (
                    '{identifier}: {field.type_} {field.name}'
                    .format(identifier=identifier, field=field)
                )
                lines += '\n'
            lines += '}\n'
        lines = lines.strip()
        return lines
