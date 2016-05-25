import re

from collections import OrderedDict
from .primitives import _PROTOBUF
from ..meta import FormatMeta


class Thrift(FormatMeta):
    def __init__(self, filepath):
        super(Thrift, self).__init__(filepath)

    def to_protobuf(self, serialized=False, indent=4):
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
        if serialized:
            return self._writer.write(messages, indent, fmt=self.PROTOBUF)
        return messages
