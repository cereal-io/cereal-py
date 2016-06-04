from ..formats import Format
from ..meta import FormatMeta


class Avro(FormatMeta):
    def __init__(self, filepath):
        super(Avro, self).__init__()
        self._messages = self._reader.read(filepath)

    @property
    def messages(self):
        return self._messages

    def to_protobuf(self, indent=4):
        """Convert an Apache Avro file to a Google Protocol Buffer file.
        """
        return self._writer.write(self._messages, indent, to=Format.PROTOBUF)

    def to_thrift(self, indent=4):
        """Convert an Apache Avro file to an Apache Thrift file."""
        return self._writer.write(self._messages, indent, to=Format.THRIFT)
