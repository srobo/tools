from __future__ import print_function


def command(args):
    import sys

    import sr.tools.inventory.inventory as srinv
    import sr.tools.inventory.assetcode as assetcode
    from sr.tools.inventory.inventory import get_inventory, normalise_partcode

    inv = get_inventory()

    parts = []
    for c in args.part_code:
        code = normalise_partcode(c)

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
        print("# item -> parent")

        if hasattr(part.parent, "code"):
            print("%s -> %s" % (part.code, part.parent.code))

        elif hasattr(part.parent, "name"):
            print("%s -> dir(%s)" % (part.code, part.parent.name))


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-showparent',
                                   help='Show parent of items.')
    parser.add_argument('part_code', nargs='+', help='Part codes to show.')
    parser.set_defaults(func=command)
