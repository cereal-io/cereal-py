from ..meta import FormatMeta


class Avro(FormatMeta):
    def __init__(self, filepath):
        super(Avro, self).__init__(filepath)

    def to_protobuf(self, serialized=False, indent=4):
        """Convert an Apache Avro file to a Google Protocol Buffer file.
        """
        records = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(records, indent, to=self.PROTOBUF)
        return records

    def to_thrift(self, serialized=False, indent=4):
        """Convert an Apache Avro file to an Apache Thrift file."""
        records = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(records, indent, to=self.THRIFT)
        return records
