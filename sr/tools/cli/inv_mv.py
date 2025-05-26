def command(args):
    import os
    import subprocess
    import sys

    from sr.tools.inventory import assetcode
    from sr.tools.inventory.inventory import get_inventory

    inv = get_inventory()
    cwd = os.getcwd()

    parts = []
    seen_codes = set()
    for c in args.assetcodes:
        code = assetcode.normalise(c)

        if code in seen_codes:
            # This asset was already in an earlier argument
            continue
        seen_codes.add(code)

        try:
            assetcode.code_to_num(code)
        except ValueError:
            print(f"Error: {c} is an invalid asset code.", file=sys.stderr)
            sys.exit(1)

        try:
            part = inv.root.parts[code]
        except KeyError:
            print(f"Error: There is no part with code {code}.", file=sys.stderr)
            sys.exit(1)

        if part.parent.path == cwd:
            print(f"Warning: Part {code} is already in {cwd}.")
            continue

        if hasattr(part.parent, "code") and not args.ignore_assy:
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
        "-q",
        "--ignore-assy",
        action="store_true",
        help="Don't print warnings about items being part of an assembly.",
    )

    parser.add_argument(
        "assetcodes",
        metavar="ASSET_CODE",
        nargs="+",
        help="The asset code of the item to move.",
    )
    parser.set_defaults(func=command)
