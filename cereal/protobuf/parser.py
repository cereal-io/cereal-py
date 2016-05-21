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
            syntax = 'proto{}'.format(match.group('syntax'))
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
        start = 0
        for i, line in enumerate(lines[start:]):
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
                    identifier = match.group(1)
                    enumerations[identifier] = OrderedDict()
                    enumerations[identifier]['type'] = 'enum'
                    enumerations[identifier]['name'] = match.group(1)
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
                    start = j
                    break
                if line == '':
                    continue
                match = re.match(self._patterns['field'], line)
                if match is None:
                    # Could not match field - continue to the next line.
                    continue
                rule, t, identifier, _ = match.groups()
                try:
                    t = self.PRIMITIVES[t]
                    field = {
                        'name': identifier,
                        'type': t,
                    }
                except KeyError:
                    # Search `enumerations` for type. If the enumeration
                    # exists, then append it to the `schemas` object.
                    try:
                        enumeration = enumerations[t]
                        field = enumeration
                    except KeyError:
                        # The enumeration type was not found, therefore,
                        # continue parsing the remainder of the lines.
                        continue
                record['fields'].append(field)
            schemas.append(record)
        return json.dumps(schemas, indent=indent)
