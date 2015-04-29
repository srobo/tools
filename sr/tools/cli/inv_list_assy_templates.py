from __future__ import print_function


def command(args):
    import argparse
    import sys

    from sr.tools.cli import inv_list_templates

    print("'inv-list-assy-templates' is deprecated. Please use "
          "'inv-list-templates --assemblies' instead.", file=sys.stderr)

    args = argparse.Namespace()
    args.assemblies = True
    inv_list_templates.command(args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-list-assy-templates',
                                   help='List assembly templates.')
    parser.set_defaults(func=command)
