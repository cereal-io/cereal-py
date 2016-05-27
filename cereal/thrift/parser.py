from ..meta import FormatMeta


class Thrift(FormatMeta):
    def __init__(self, filepath):
        super(Thrift, self).__init__(filepath)

    def to_protobuf(self, serialized=False, indent=4):
        """Convert an Apache Thrift file to a Google Protocol Buffer
        file."""
        messages = self._reader.read(self._filepath, to=self.PROTOBUF)
        if serialized:
            return self._writer.write(messages, indent, fmt=self.PROTOBUF)
        return messages
