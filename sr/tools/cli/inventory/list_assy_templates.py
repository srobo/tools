from __future__ import print_function


def command(args):
    import os
    import sys

    from sr.tools.inventory.oldinv import gettoplevel

    gitdir = gettoplevel()
    if not gitdir:
        # Not in the inventory, give up
        sys.exit(1)

    templatedir = os.path.join(gitdir, ".meta", "assemblies")
    templates = os.listdir(templatedir)

    for template in templates:
        if template in ["default"]:
            continue

        print(template)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-list-assy-templates',
                                   help='List assembly templates.')
    parser.set_defaults(func=command)
