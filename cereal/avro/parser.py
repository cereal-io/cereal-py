from ..formats import Format
from ..meta import FormatMeta


class Avro(FormatMeta):
    def __init__(self, filepath):
        super(Avro, self).__init__()
        self._records = self._reader.read(filepath)

    @property
    def record(self):
        return self._records

    def to_protobuf(self, serialized=False, indent=4):
        """Convert an Apache Avro file to a Google Protocol Buffer file.
        """
        if serialized:
            return self._writer.write(self._records, indent,
                                      to=Format.PROTOBUF)
        return self._records

    def to_thrift(self, serialized=False, indent=4):
        """Convert an Apache Avro file to an Apache Thrift file."""
        if serialized:
            return self._writer.write(self._records, indent, to=Format.THRIFT)
        return self._records
