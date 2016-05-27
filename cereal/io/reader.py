import json
import re

from collections import OrderedDict
from ..primitives import Avro
from ..primitives import Protobuf
from ..primitives import Thrift


class Reader(object):
    def __init__(self, fmt, patterns=None):
        if patterns is None:
            patterns = {}
        self._fmt = fmt
        self._patterns = patterns
        self._primitives = {
            'avro': Avro,
            'protobuf': Protobuf,
            'thrift': Thrift,
        }[fmt]

    def read(self, filepath, to=None):
        extension = re.match(r'^.*\.(?P<extension>\w+)$', filepath)
        extension = extension.group('extension')
        fn = {
            'avsc': self._from_avro,
            'proto': self._from_protobuf,
            'thrift': self._from_thrift,
        }[extension]
        return fn(filepath, to=to.upper())

    def _from_avro(self, filepath, to=None):
        with open(filepath) as fp:
            records = json.loads(fp.read())
        primitives = getattr(self._primitives, '_{to}'.format(to=to))
        for record in records:
            for field in record['fields']:
                t = field['type']
                try:
                    t = primitives[t]
                except KeyError:
                    continue
                field['type'] = t
        return records

    def _from_protobuf(self, filepath, to=None):
        with open(filepath) as fp:
            lines = fp.readlines()
        primitives = getattr(self._primitives, '_{to}'.format(to=to))
        schemas = []
        for i, line in enumerate(lines):
            line = line.strip()
            match = re.match(self._patterns['message'], line)
            if match is None:
                continue
            record = OrderedDict()
            record['type'] = 'record'
            # Google Protocol Buffer message name.
            record['name'] = match.group('name')
            record['fields'] = []
            enumerations = {}
            j = i
            while True:
                # Increment `j` by 1 to ignore the `message` line
                # itself.
                j += 1
                line = lines[j].strip()
                match = re.match(self._patterns['enumeration'], line)
                if match is not None:
                    # Detected an enumeration type.
                    identifier = match.group('enumeration')
                    enumerations[identifier] = OrderedDict()
                    enumerations[identifier]['type'] = 'enum'
                    enumerations[identifier]['name'] = identifier
                    enumerations[identifier]['symbols'] = []
                    while True:
                        # Omit `enum` field declaration.
                        j += 1
                        line = lines[j].strip()
                        if line.endswith('}'):
                            # Omit ending curly brace of enumerated
                            # type.
                            j += 1
                            break
                        symbols = line.split()
                        enumerations[identifier]['symbols'].append(symbols[0])
                line = lines[j].strip()
                if line.endswith('}'):
                    break
                if line == '':
                    continue
                match = re.match(self._patterns['field'], line)
                if match is None:
                    # Could not match field - continue to the next line.
                    continue
                rule, t, identifier, _ = match.groups()
                try:
                    t = primitives[t]
                    field = {
                        'name': identifier,
                        'type': t,
                    }
                except KeyError:
                    # Search `enumerations` for type. If the enumeration
                    # exits, then append it to the `schemas` object.
                    try:
                        enumeration = enumerations[t]
                        field = enumeration
                    except KeyError:
                        # The enumeration type was not found, therefore,
                        # continue parsing the remainder of the lines.
                        continue
                record['fields'].append(field)
            schemas.append(record)
        return schemas

    def _from_thrift(self, filepath, to=None):
        with open(filepath) as fp:
            lines = fp.readlines()
        primitives = getattr(self._primitives, '_{to}'.format(to=to))
        messages = []
        for i, line in enumerate(lines):
            message = {}
            line = line.strip()
            match = re.match(self._patterns['struct'], line)
            if match is None:
                continue
            message = OrderedDict()
            message['identifier'] = match.group('struct')
            message['fields'] = []
            j = i
            while not line.endswith('}'):
                j += 1
                line = lines[j].strip()
                if line == '':
                    continue
                match = re.match(self._patterns['field'], line)
                if match is None:
                    continue
                identifier, t, name = match.groups()
                try:
                    t = primitives[t]
                except KeyError:
                    continue
                field = {
                    'identifier': int(identifier),
                    'type': t,
                    'name': name,
                }
                message['fields'].append(field)
            messages.append(message)
        return messages
