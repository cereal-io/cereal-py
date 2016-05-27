from ..meta import FormatMeta


class Avro(FormatMeta):
    def __init__(self, filepath):
        super(Avro, self).__init__(filepath)

    def to_protobuf(self, serialized=False, indent=4):
        records = self._reader.read(self._filepath, to=self.PROTOBUF)
        if serialized:
            return self._writer.write(records, indent, fmt=self.PROTOBUF)
        return records
