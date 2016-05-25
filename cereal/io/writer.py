class Writer(object):
    """Agnostic class used to generate standard output from any format."""
    def write(self, objects, indent, fmt=None):
        return {
            'protobuf': self._to_protobuf
        }[fmt](objects, indent)

    def _to_protobuf(self, objects, indent):
        """Return serialized protocol buffers."""
        first = 0
        last = len(objects) - 1
        lines = ''
        for i, object in enumerate(objects):
            lines += '\n' if i != first else ''
            # The `message` name can either be indexed via the `name`
            # key or the `identifier` depending on the object type.
            try:
                message = object['name']
            except KeyError:
                message = object['identifier']
            lines += 'message {}'.format(message)
            lines += ' {\n'
            fields = object['fields']
            for j, field in enumerate(fields):
                identifier = field.get('identifier', j + 1)
                lines += ' ' * indent + (
                    '{field[type]} {field[name]} = {identifier};\n'
                    .format(field=field, identifier=identifier)
                )
            lines += '}\n' if i != last else '}'
        return lines
