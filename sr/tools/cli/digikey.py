from __future__ import print_function


def command(args):
    import io
    import sys

    import sr.tools.bom.digikey as digikey

    if args.id:
        ids_stream = io.StringIO('\n'.join(args.id))
    else:
        print('Reading from stdin.', file=sys.stderr)
        ids_stream = sys.stdin

    line = ids_stream.readline()
    while line:
        item = digikey.Item(line.strip())
        item.print_info()
        line = ids_stream.readline()


def add_subparser(subparsers):
    parser = subparsers.add_parser('digikey',
                                   help='Get information about a part '
                                        'from DigiKey.')
    parser.add_argument('id', nargs='*', help='IDs to get information about.')
    parser.set_defaults(func=command)
