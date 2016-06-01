import json
import os
import re

from ..models import Enumeration
from ..models import Field
from ..models import Message


class Reader(object):
    def __init__(self, fmt):
        filepath = os.path.join(os.path.dirname(__file__), '../common.json')
        with open(filepath) as fp:
            common = json.loads(fp.read())
        # Try to load the associated regular expression patterns from
        # key based on the lowercased class name.
        self._primitives = common[fmt]['primitives']
        self._patterns = common[fmt].get('patterns', {})

    def read(self, filepath):
        extension = re.match(r'^.*\.(?P<extension>\w+)$', filepath)
        extension = extension.group('extension')
        fn = {
            'avsc': self._from_avro,
            'proto': self._from_protobuf,
            'thrift': self._from_thrift,
        }[extension]
        filepath = os.path.expanduser(filepath)
        return fn(filepath)

    def _from_avro(self, filepath):
        """Read a '.avsc' file and convert the contents to common cereal
        format."""
        with open(filepath) as fp:
            records = json.loads(fp.read())
        messages = []
        for record in records:
            message = Message()
            message.name = record['name']
            fields = record['fields']
            # To avoid name clashing, the `enumerate` function is used
            # to maintain the index of the array.
            for i, _ in enumerate(fields):
                if fields[i]['type'] in self._primitives:
                    # The field is a native data type.
                    field = Field()
                    field.name = fields[i]['name']
                    field.type_ = fields[i]['type']
                    message.fields.append(field)
                else:
                    if fields[i]['type'] == 'enum':
                        # The field is an enumeration type.
                        enumeration = Enumeration()
                        enumeration.name = fields[i]['name']
                        enumeration.symbols = fields[i]['symbols']
                        message.fields.append(enumeration)
            messages.append(message)
        return messages

    def _from_protobuf(self, filepath):
        """Read a '.proto' file and convert the contents to common
        cereal format."""
        with open(filepath) as fp:
            lines = fp.readlines()
        messages = []
        for i, line in enumerate(lines):
            line = line.strip()
            match = re.match(self._patterns['message'], line)
            if match is None:
                continue
            message = Message()
            # Google Protocol Buffer message name.
            message.name = match.group('name')
            j = i
            while True:
                # Increment `j` by 1 to ignore the `message` line
                # itself.
                j += 1
                line = lines[j].strip()
                match = re.match(self._patterns['enumeration'], line)
                if match is not None:
                    # Detected an enumeration type.
                    enumeration = Enumeration()
                    identifier = match.group('enumeration')
                    enumeration.name = identifier
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
                        enumeration.symbols.append(symbols[0])
                    message.fields.append(enumeration)
                    # Continue to the next field to prevent creating
                    # another field with the enumeration properties.
                    continue
                line = lines[j].strip()
                if line.endswith('}'):
                    break
                if line == '':
                    continue
                match = re.match(self._patterns['field'], line)
                if match is None:
                    # Could not match field - continue to the next line.
                    continue
                rule, t, name, identifier = match.groups()
                field = Field()
                field.rule = rule
                field.type_ = t
                field.name = name
                field.identifier = int(identifier)
                message.fields.append(field)
            messages.append(message)
        return messages

    def _from_thrift(self, filepath):
        with open(filepath) as fp:
            lines = fp.readlines()
        messages = []
        for i, line in enumerate(lines):
            line = line.strip()
            match = re.match(self._patterns['struct'], line)
            if match is None:
                continue
            message = Message()
            message.name = match.group('struct')
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
                field = Field()
                field.identifier = int(identifier)
                field.type_ = t
                field.name = name
                message.fields.append(field)
            messages.append(message)
        return messages
