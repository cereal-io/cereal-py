import json
import os


class ProtocolMeta(object):
    def __init__(self, filepath):
        self._filepath = os.path.expanduser(filepath)
        name = os.path.join(os.path.dirname(__file__), 'patterns.json')
        with open(name) as fp:
            context = json.loads(fp.read())
        try:
            # Try to load the associated patterns key/value pair based
            # on the lowercased class name.
            key = self.__class__.__name__.lower()
            patterns = context[key]
        except KeyError:
            patterns = {}
        self._patterns = patterns

    @property
    def patterns(self):
        return self._patterns
