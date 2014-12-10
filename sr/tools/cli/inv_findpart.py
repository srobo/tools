from __future__ import print_function


def command(args):
    import os
    import sys

    from sr.tools.inventory import assetcode
    from sr.tools.inventory.inventory import get_inventory

    ASSET_CODE = 0
    PART_TYPE = 1

    COLOUR_RESET = "\033[0m"
    COLOUR_GREEN = "\033[1;32m"
    COLOUR_RED = "\033[1;31m"
    COLOUR_YELLOW = "\033[1;33m"

    inv = get_inventory()

    parts = []
    spec_type = ASSET_CODE
    for c in args.itemspecs:
        code = assetcode.normalise(c)

        try:
            assetcode.code_to_num(code)
            spec_type = ASSET_CODE
        except:
            if c in inv.root.types:
                spec_type = PART_TYPE
            else:
                print("Error: %s is an invalid asset code or part type." %
                      c, file=sys.stderr)
                sys.exit(1)

        if spec_type == ASSET_CODE:
            try:
                part = inv.root.parts[code]
            except KeyError:
                print("Error: There is no part with code %s." %
                      code, file=sys.stderr)
                sys.exit(1)

            parts.append(part)
        else:
            try:
                parts.extend(inv.root.types[c])
            except:
                print("Error: There is no part type %s." % c, file=sys.stderr)
                sys.exit(1)

    stat_colour = ""
    path = ""
    for part in parts:
        if args.relpath:
            path = os.path.relpath(part.path)
        else:
            path = part.path

        if args.asset_stat and hasattr(part, "condition"):
            if part.condition == "broken":
                stat_colour = COLOUR_RED
            elif part.condition == "unknown":
                stat_colour = COLOUR_YELLOW
            elif part.condition == "working":
                stat_colour = COLOUR_GREEN
            print(path, stat_colour, part.condition, COLOUR_RESET)
        else:
            print(path)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-findpart',
                                   help='Find the location of a specific item '
                                        'in the inventory.')
    parser.add_argument("-s", "--stat", action="store_true", default=False,
                        dest="asset_stat",
                        help="Show the status of each asset listed based upon "
                             "the 'condition' field.")
    parser.add_argument("-r", "--relpath", action="store_true", default=False,
                        dest="relpath",
                        help="Print relative, rather than absolute, paths.")
    parser.add_argument("itemspecs", metavar="ITEM_SPEC", nargs="+",
                        help="Either an SR asset code or part type. "
                             "The nature of the specifier is auto-detected "
                             "and asset codes/part types can be mixed.")
    parser.set_defaults(func=command)
