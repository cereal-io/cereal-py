import os


class ProtocolMeta(object):
    def __init__(self, filepath):
        self._filepath = os.path.expanduser(filepath)
