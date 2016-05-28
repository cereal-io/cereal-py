import json
import re

from collections import namedtuple
from collections import OrderedDict


class Reader(object):
    def __init__(self, patterns=None):
        if patterns is None:
            patterns = {}
        self._patterns = patterns

    def read(self, filepath):
        extension = re.match(r'^.*\.(?P<extension>\w+)$', filepath)
        extension = extension.group('extension')
        fn = {
            'avsc': self._from_avro,
            'proto': self._from_protobuf,
            'thrift': self._from_thrift,
        }[extension]
        return fn(filepath)

    def _from_avro(self, filepath):
        with open(filepath) as fp:
            records = json.loads(fp.read())
        return records

    def _from_protobuf(self, filepath):
        with open(filepath) as fp:
            lines = fp.readlines()
        messages = []
        enumerations = {}
        for i, line in enumerate(lines):
            line = line.strip()
            match = re.match(self._patterns['message'], line)
            if match is None:
                continue
            message = OrderedDict()
            # Google Protocol Buffer message name.
            message['name'] = match.group('name')
            message['fields'] = []
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
                field = {
                    'rule': rule,
                    'name': identifier,
                    'type': t,
                }
                message['fields'].append(field)
            messages.append(message)
        return messages

    def _from_thrift(self, filepath):
        with open(filepath) as fp:
            lines = fp.readlines()
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
                field = {
                    'identifier': int(identifier),
                    'type': t,
                    'name': name,
                }
                message['fields'].append(field)
            messages.append(message)
        return messages
