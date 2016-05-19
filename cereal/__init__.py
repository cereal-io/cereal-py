import re

from .protobuf.parser import Protobuf
from .avro.parser import Avro
from .exceptions import UnknownExtensionError


def build(filepath):
    match = re.match(r'^.*\.(?P<extension>\w+)$', filepath)
    if match is None:
        return
    extension = match.group('extension')
    try:
        return {
            'proto': Protobuf(filepath),
            'avsc': Avro(filepath),
        }[extension]
    except KeyError:
        raise UnknownExtensionError(extension)
