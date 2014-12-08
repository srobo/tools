from __future__ import print_function


def command(args):
    import sys

    import sr.tools.inventory.query as query
    from pyparsing import ParseException

    query_str = args.query
    style = 'codes' if args.codes else 'paths'
    verbose = args.v

    try:

        count = 0
        for asset in query.query(query_str):
            count += 1
            print(asset.code if style == 'codes' else asset.path)
        if verbose:
            print("# {0} results".format(count), file=sys.stderr)
    except ParseException as e:
        print("Query Error:", e, file=sys.stderr)
        sys.exit(1)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-query',
                                   help='Perform query on the inventory')
    parser.add_argument('--codes', action='store_true')
    parser.add_argument('--paths', action='store_true')
    parser.add_argument('-v', action='store_true')
    parser.add_argument('query')
    parser.set_defaults(func=command)
