import re

from .avro.parser import Avro
from .protobuf.parser import Protobuf
from .thrift.parser import Thrift
from .exceptions import UnknownExtensionError


def build(filepath):
    match = re.match(r'^.*\.(?P<extension>\w+)$', filepath)
    extension = match.group('extension')
    try:
        svc = {
            'avsc': Avro(filepath),
            'proto': Protobuf(filepath),
            'thrift': Thrift(filepath),
        }[extension]
    except KeyError:
        raise UnknownExtensionError(extension)
    return svc
