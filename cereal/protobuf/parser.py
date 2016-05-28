import re

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
        """Convert a Google Protocol Buffer file to an Apache Avro file.
        """
        schemas = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(schemas, indent=indent, to=self.AVRO)
        return schemas

    def to_thrift(self, serialized=False, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Thrift
        file."""
        schemas = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(schemas, indent=indent, to=self.THRIFT)
        return schemas
