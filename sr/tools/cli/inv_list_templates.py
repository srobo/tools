from __future__ import print_function


def command(args):
    import os

    from sr.tools.inventory.inventory import get_inventory

    inventory = get_inventory()
    templatedir = os.path.join(inventory.root_path, ".meta",
                               'assemblies' if args.assemblies else 'parts')
    templates = os.listdir(templatedir)

    for template in templates:
        if template in ["default"]:
            continue

        print(template)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-list-templates',
                                   help='List inventory templates.')
    parser.add_argument('--parts', '-p', action='store_true', dest='parts',
                        default=True)  # doesn't actually do anything
    parser.add_argument('--assemblies', '-a', action='store_true',
                        dest='assemblies')
    parser.set_defaults(func=command)
