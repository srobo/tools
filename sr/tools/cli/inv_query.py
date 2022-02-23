def command(args):
    import sys

    from pyparsing import ParseException

    from sr.tools.inventory.inventory import get_inventory

    inventory = get_inventory()

    query_str = args.query
    style = 'codes' if args.codes else 'paths'
    verbose = args.v

    try:
        count = 0
        for asset in inventory.query(query_str):
            count += 1
            print(asset.code if style == 'codes' else asset.path)
        if verbose:
            print(f"# {count} results", file=sys.stderr)
    except ParseException as e:
        print("Query Error:", e, file=sys.stderr)
        sys.exit(1)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-query', help='Perform query on the inventory')
    parser.add_argument('--codes', action='store_true')
    parser.add_argument('--paths', action='store_true')
    parser.add_argument('-v', action='store_true')
    parser.add_argument('query')
    parser.set_defaults(func=command)
