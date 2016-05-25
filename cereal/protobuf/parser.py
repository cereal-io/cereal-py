import json
import re

from collections import OrderedDict
from .primitives import _AVRO
from .primitives import _THRIFT
from ..meta import FormatMeta


class Protobuf(FormatMeta):
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

    def to_avro(self, serialized=False, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Avro file."""
        with open(self._filepath) as fp:
            lines = fp.readlines()
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
                    t = _AVRO[t]
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
        if serialized:
            return json.dumps(schemas, indent=indent)
        return schemas
