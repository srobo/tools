from __future__ import print_function


def command(args):
    import sys

    from sr.tools.inventory import assetcode
    from sr.tools.inventory.inventory import get_inventory
    from sr.tools.environment import open_editor

    inv = get_inventory()

    parts = []
    for c in args.part_code:
        code = assetcode.normalise(c)

        try:
            assetcode.code_to_num(code)
        except:
            print("Error: %s is an invalid code." % code, file=sys.stderr)
            sys.exit(1)

        try:
            part = inv.root.parts[code]
        except KeyError:
            print("Error: There is no part with code %s." %
                  code, file=sys.stderr)
            sys.exit(1)

        parts.append(part)

    for part in parts:
        open_editor(part.path)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-edit',
                                   help='Edit inventory items by part code.')
    parser.add_argument('part_code', nargs='+', help='Part codes to edit.')
    parser.set_defaults(func=command)
