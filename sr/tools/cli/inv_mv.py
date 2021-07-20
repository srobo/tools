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
            print(f"Error: {c} is an invalid asset code.", file=sys.stderr)
            sys.exit(1)

        try:
            part = inv.root.parts[code]
        except:
            print(f"Error: There is no part with code {code}.", file=sys.stderr)
            sys.exit(1)

        if part.parent.path == cwd:
            print(f"Warning: Part {code} is already in {cwd}.")
            continue

        if hasattr(part.parent, "code"):
            if args.assy:
                parts.append(part.parent)
            else:
                print(
                    f"Warning: Part {code} is in an assembly.",
                    "To move the assembly, use the -a switch.",
                    file=sys.stderr,
                )
                parts.append(part)

        else:
            parts.append(part)

    if parts:
        paths = [x.path for x in parts]
        subprocess.check_call(['git', 'mv'] + paths + ['.'])
    else:
        print("Warning: No parts to move", file=sys.stderr)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-mv', help="Move inventory items into the CWD.")
    parser.add_argument(
        "-a",
        "--assy",
        action="store_true",
        default=False,
        dest="assy",
        help="If the asset codes are part of an assembly then "
        "move the whole assembly.",
    )
    parser.add_argument(
        "assetcodes",
        metavar="ASSET_CODE",
        nargs="+",
        help="The asset code of the item to move.",
    )
    parser.set_defaults(func=command)
