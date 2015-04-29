from __future__ import print_function


def command(args):
    import io
    import sys

    import sr.tools.bom.farnell as farnell

    if args.id:
        ids_stream = io.StringIO('\n'.join(args.id))
    else:
        print('Reading from stdin.', file=sys.stderr)
        ids_stream = sys.stdin

    line = ids_stream.readline()
    while line:
        item = farnell.Item(line.strip())
        item.print_info()
        line = ids_stream.readline()


def add_subparser(subparsers):
    parser = subparsers.add_parser('farnell',
                                   help='Get information about a part from '
                                        'Farnell.')
    parser.add_argument('id', nargs='*', help='IDs to get information about.')
    parser.set_defaults(func=command)
