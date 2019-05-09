from __future__ import print_function


def command(args):
    import os
    import subprocess
    import sys

    from sr.tools.inventory import assetcode
    from sr.tools.inventory.inventory import get_inventory

    inv = get_inventory()
    cwd = os.getcwd()

    parts = []
    for c in args.assetcodes:
        code = assetcode.normalise(c)

        try:
            assetcode.code_to_num(code)
        except:
            print("Error: {} is an invalid asset code.".format(c),
                  file=sys.stderr)
            sys.exit(1)

        try:
            part = inv.root.parts[code]
        except:
            print("Error: There is no part with code {}.".format(code),
                  file=sys.stderr)
            sys.exit(1)

        if part.parent.path == cwd:
            print("Warning: Part {} is already in {}.".format(code, cwd))
            continue

        if hasattr(part.parent, "code"):
            if args.assy:
                parts.append(part.parent)
            else:
                print("Warning: Part {} is in an assembly.".format(code),
                      "To move the assembly, use the -a switch.",
                      file=sys.stderr)
                parts.append(part)

        else:
            parts.append(part)

    if parts:
        paths = [x.path for x in parts]
        subprocess.check_call(['git', 'mv'] + paths + ['.'])
    else:
        print("Warning: No parts to move", file=sys.stderr)

def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-mv',
                                   help="Move inventory items into the CWD.")
    parser.add_argument("-a", "--assy", action="store_true", default=False,
                        dest="assy",
                        help="If the asset codes are part of an assembly then "
                             "move the whole assembly.")
    parser.add_argument("assetcodes", metavar="ASSET_CODE",
                        nargs="+", help="The asset code of the item to move.")
    parser.set_defaults(func=command)
