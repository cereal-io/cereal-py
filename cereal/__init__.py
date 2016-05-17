import re

from .protobuf.parser import Protobuf
from .avro.parser import Avro
from .exceptions import UnknownExtensionError


def build(filepath):
    prog = re.compile(r'^.*\.(\w+)$')
    match = prog.match(filepath)
    if match is not None:
        extension = match.group(1)
        try:
            return {
                'proto': Protobuf(filepath),
                'avsc': Avro(filepath),
            }[extension]
        except KeyError:
            raise UnknownExtensionError(extension)
