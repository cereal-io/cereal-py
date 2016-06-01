from ..formats import Format
from ..meta import FormatMeta


class Protobuf(FormatMeta):
    def __init__(self, filepath):
        super(Protobuf, self).__init__(filepath)

    def to_avro(self, serialized=False, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Avro file.
        """
        schemas = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(schemas, indent=indent, to=Format.AVRO)
        return schemas

    def to_thrift(self, serialized=False, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Thrift
        file."""
        schemas = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(schemas, indent=indent,
                                      to=Format.THRIFT)
        return schemas
