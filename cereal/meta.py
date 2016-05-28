import json
import os

from .io.reader import Reader
from .io.writer import Writer


class FormatMeta(object):
    AVRO = 'avro'
    PROTOBUF = 'protobuf'
    THRIFT = 'thrift'

    def __init__(self, filepath):
        self._filepath = os.path.expanduser(filepath)
        name = os.path.join(os.path.dirname(__file__), 'patterns.json')
        with open(name) as fp:
            patterns = json.loads(fp.read())
        fmt = self.__class__.__name__.lower()
        # Try to load the associated regular expression patterns from
        # key based on the lowercased class name.
        patterns = patterns.get(fmt, {})
        self._reader = Reader(patterns=patterns)
        self._writer = Writer(fmt)
        self._patterns = patterns

    @property
    def patterns(self):
        return self._patterns
