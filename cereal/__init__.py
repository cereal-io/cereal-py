import re

from .avro.parser import Avro
from .protobuf.parser import Protobuf
from .thrift.parser import Thrift
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
            'thrift': Thrift(filepath),
        }[extension]
    except KeyError:
        raise UnknownExtensionError(extension)
