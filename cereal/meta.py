import os


class ProtocolMeta(object):
    def __init__(self, filepath):
        self._filepath = os.path.expanduser(filepath)

    def __repr__(self):
        if self.__class__.__name__.lower() == 'protobuf':
            return '<{}:{}>'.format(self.__class__.__name__, self._syntax)
        else:
            return '<{}>'.format(self.__class__.__name__)
