import re

from collections import OrderedDict
from primitives import _PROTOBUF
from ..meta import ProtocolMeta


class Thrift(ProtocolMeta):
    def __init__(self, filepath):
        super(Thrift, self).__init__(filepath)

    def to_protobuf(self, indent=4):
        """Convert an Apache Thrift file to a Google Protocol Buffer
        file."""
        with open(self._filepath) as fp:
            lines = fp.readlines()
        messages = []
        for i, line in enumerate(lines):
            message = {}
            line = line.strip()
            match = re.match(self._patterns['struct'], line)
            if match is None:
                continue
            message = OrderedDict()
            message['identifier'] = match.group(1)
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
                    t = _PROTOBUF[t]
                except KeyError:
                    continue
                field = {
                    'identifier': int(identifier),
                    'type': t,
                    'name': name,
                }
                message['fields'].append(field)
            messages.append(message)
        context = ''
        for message in messages:
            context += 'message {}'.format(message['identifier'])
            context += ' {\n'
            for field in message['fields']:
                context += ' ' * indent + (
                    '{field[type]} {field[name]} = {field[identifier]}'
                    .format(field=field)
                )
                context += '\n'
            context += '}\n'
        return context
