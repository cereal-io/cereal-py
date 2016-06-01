import os

from .io.reader import Reader
from .io.writer import Writer


class FormatMeta(object):
    def __init__(self, filepath):
        self._filepath = os.path.expanduser(filepath)
        fmt = self.__class__.__name__.lower()
        self._reader = Reader(fmt)
        self._writer = Writer(fmt)
