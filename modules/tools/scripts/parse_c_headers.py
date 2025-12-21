from enum import Enum

import sys

import CppHeaderParser.CppHeaderParser as chp


class Types(str, Enum):
    struct = 's'
    enum = 'e'
    union = 'u'
    typedef = 't'
    macro = 'm'
    function = 'f'
    variable = 'v'
    constant = 'o'


def main():
    # Using: tool.py <header_file> [-o <output_file>] [-t <types>] [-I <include_path>]
    output_file = None
    header_file = None
    types = {Types.macro}
    includes = []

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '-o':
            output_file = sys.argv[(i := i+1)]

        elif arg == '-t':
            types = set(sys.argv[(i := i+1)])

        elif arg == '-I':
            includes.append(sys.argv[(i := i+1)])

        else:
            if header_file is not None:
                print("Error: Too many arguments")
                return

            header_file = sys.argv[i]

        i += 1

    del i, arg

    header = chp.CppHeader(header_file)

    if Types.constant in types:
        for name, value in header.defines.items():
            print(name, value)


