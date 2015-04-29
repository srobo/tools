from __future__ import print_function


def command(args):
    import sys

    from sr.tools.inventory import assetcode
    from sr.tools.inventory.inventory import get_inventory

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
        print("# item -> parent")

        if hasattr(part.parent, "code"):
            print("%s -> %s" % (part.code, part.parent.code))

        elif hasattr(part.parent, "name"):
            print("%s -> dir(%s)" % (part.code, part.parent.name))


def command_deprecated(args):
    import sys

    print("This is deprecated, please use 'inv-show-parent' instead.",
          file=sys.stderr)
    command(args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-showparent',
                                   help='Show parent of items.')
    parser.add_argument('part_code', nargs='+', help='Part codes to show.')
    parser.set_defaults(func=command_deprecated)

    parser = subparsers.add_parser('inv-show-parent',
                                   help='Show parent of items.')
    parser.add_argument('part_code', nargs='+', help='Part codes to show.')
    parser.set_defaults(func=command)
