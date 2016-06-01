from ..formats import Format
from ..meta import FormatMeta


class Protobuf(FormatMeta):
    def __init__(self, filepath):
        super(Protobuf, self).__init__()
        self._schemas = self._reader.read(filepath)

    @property
    def schemas(self):
        return self._schemas

    def to_avro(self, serialized=False, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Avro file.
        """
        if serialized:
            return self._writer.write(self._schemas, indent=indent,
                                      to=Format.AVRO)
        return self._schemas

    def to_thrift(self, serialized=False, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Thrift
        file."""
        if serialized:
            return self._writer.write(self._schemas, indent=indent,
                                      to=Format.THRIFT)
        return self._schemas
