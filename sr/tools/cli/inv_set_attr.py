from __future__ import print_function


def replace_line(path, key, value):
    import re

    print("Replacing:", key, "->", value, "in", path)
    pattern = r"{key}( *):( *)(?:[^#\s]*)(.*)".format(key=key)

    with open(path) as fd:
        lines = list(fd)

    for i, line in enumerate(lines):
        match = re.match(pattern, line)
        if match is not None:
            lines[i] = "{key}{0}:{1}{value}{2}\n".format(*match.groups(),
                                                         key=key, value=value)
            break
    else:
        lines.append("{}: {}\n".format(key, value))

    with open(path, "w") as fd:
        for line in lines:
            fd.write(line)


def command(args):
    import sys

    from sr.tools.inventory import assetcode
    from sr.tools.inventory.inventory import get_inventory

    inv = get_inventory()

    for code in args.asset:
        part = inv.root.parts[assetcode.normalise(code)]
        if part is not None:
            replace_line(part.info_path, args.attrname, args.attrvalue)
        else:
            print("Could not find asset:", code, file=sys.stderr)
            sys.exit(1)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-set-attr',
                                   help="Sets an attribute on one or more "
                                        "items or assemblies.")
    parser.add_argument('attrname', type=str,
                        help="The name of the attribute.")
    parser.add_argument('attrvalue', type=str, help="The value to set.")
    parser.add_argument('asset', type=str, nargs='+',
                        help="The codes of the assets to modify.")
    parser.set_defaults(func=command)
