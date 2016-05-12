#!/usr/bin/env python

import argparse
import json
import os
import re

from collections import OrderedDict

# type definitions for .proto to Java
types = {
    'double': 'double',
    'float': 'float',
    'int32': 'int',
    'int64': 'long',
    'uint32': 'int',
    'uint64': 'long',
    'sint32': 'int',
    'sint64': 'long',
    'fixed32': 'int',
    'fixed64': 'long',
    'sfixed32': 'int',
    'sfixed64': 'long',
    'bool': 'boolean',
    'string': 'String',
    'bytes': 'ByteString',
}


def parse(args):
    """Convert a Google Protocol Buffer file to an Apache Avro file."""
    name = os.path.expanduser(args.f)
    with open(name) as fp:
        schemas = []
        lines = fp.readlines()
        prog = re.compile(r'^message\s(\w+)\s\{$')
        for i in range(len(lines)):
            line = lines[i].strip()
            match = prog.match(line)
            if match:
                record = OrderedDict()
                record['type'] = 'record'
                # Google Protocol Buffer message name.
                record['name'] = match.group(1)
                record['fields'] = []
                j = i
                while True:
                    # Increment `j` by 1 to ignore the `message` line
                    # itself.
                    j += 1
                    line = lines[j].strip()
                    if line == '':
                        continue
                    if line.endswith('}'):
                        break
                    field = line.split()
                    t, identifier = field[:2]
                    try:
                        t = types[t]
                    except KeyError:
                        continue
                    record['fields'].append({
                        'name': identifier,
                        'type': t,
                    })
                schemas.append(record)
        if args.out:
            filepath = os.path.expanduser(args.out)
            with open(filepath, 'w') as fp:
                context = json.dumps(schemas, indent=4,
                                     separators=(',', ': '))
                fp.write(context)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=parse.__doc__)
    parser.add_argument('-f', type=str,
                        help='Path to Google Protocol Buffer file',
                        required=True)
    parser.add_argument('--out', type=str, help='Path to Avro output file')
    args = parser.parse_args()
    parse(args)
