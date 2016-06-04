from ..formats import Format
from ..meta import FormatMeta


class Protobuf(FormatMeta):
    def __init__(self, filepath):
        super(Protobuf, self).__init__()
        self._messages = self._reader.read(filepath)

    @property
    def messages(self):
        return self._messages

    def to_avro(self, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Avro file.
        """
        return self._writer.write(self._messages, indent=indent,
                                  to=Format.AVRO)

    def to_thrift(self, indent=4):
        """Convert a Google Protocol Buffer file to an Apache Thrift
        file."""
        return self._writer.write(self._messages, indent=indent,
                                  to=Format.THRIFT)
