from ..formats import Format
from ..meta import FormatMeta


class Thrift(FormatMeta):
    def __init__(self, filepath):
        super(Thrift, self).__init__(filepath)

    def to_avro(self, serialized=False, indent=4):
        """Convert an Apache Thrift file to an Apache Avro file."""
        messages = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(messages, indent, to=Format.AVRO)
        return messages

    def to_protobuf(self, serialized=False, indent=4):
        """Convert an Apache Thrift file to a Google Protocol Buffer
        file."""
        messages = self._reader.read(self._filepath)
        if serialized:
            return self._writer.write(messages, indent, to=Format.PROTOBUF)
        return messages
