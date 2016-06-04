from ..formats import Format
from ..meta import FormatMeta


class Thrift(FormatMeta):
    def __init__(self, filepath):
        super(Thrift, self).__init__()
        self._messages = self._reader.read(filepath)

    @property
    def messages(self):
        return self._messages

    def to_avro(self, indent=4):
        """Convert an Apache Thrift file to an Apache Avro file."""
        return self._writer.write(self._messages, indent, to=Format.AVRO)

    def to_protobuf(self, indent=4):
        """Convert an Apache Thrift file to a Google Protocol Buffer
        file."""
        return self._writer.write(self._messages, indent, to=Format.PROTOBUF)
