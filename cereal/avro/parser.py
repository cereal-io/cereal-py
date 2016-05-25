import json
import re

from collections import OrderedDict
from .primitives import _TO_PROTOBUF
from ..meta import FormatMeta


class Avro(FormatMeta):
    def __init__(self, filepath):
        super(Avro, self).__init__(filepath)

    def to_protobuf(self, serialized=False, indent=4):
        with open(self._filepath) as fp:
            records = json.loads(fp.read())
        if serialized:
            return self._writer.write(records, indent, fmt=self.PROTOBUF)
        return records
