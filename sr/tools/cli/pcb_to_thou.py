from __future__ import print_function


def command(args):
    from decimal import Decimal
    import re

    with open(args.pcb_file) as file:
        fcontent = file.read()

    def conv_ht(match):
        if match.groups()[0][0] == '"':
            return match.groups()[0]

        mm = Decimal(match.groups()[1])
        return str(int(mm / Decimal("0.000254")))

    with open(args.pcb_file, "w") as file:
        file.write(re.sub(r'(([0-9.]+)(mm)|".*?")', conv_ht, fcontent))


def add_subparser(subparsers):
    parser = subparsers.add_parser('pcb-to-thou',
                                   help='Converts all units suffixed with mm '
                                        'to hundreths of thou')
    parser.add_argument('pcb_file', help='PCB file to convert.')
    parser.set_defaults(func=command)
