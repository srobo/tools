from __future__ import print_function

import argparse
import pkg_resources

from sr.tools.cli import budget, cmds, git, ide, inventory, misc, spending, trac


def print_version():
    version = pkg_resources.get_distribution('sr.tools').version
    print("SR Tools {version}".format(version=version))


def main():
    parser = argparse.ArgumentParser(description='Student Robotics tools')
    parser.add_argument('--version', '-v', help='Show version of the tools.',
                        action='store_true')

    subparsers = parser.add_subparsers()
    budget.add_subparsers(subparsers)
    cmds.add_subparsers(subparsers)
    git.add_subparsers(subparsers)
    ide.add_subparsers(subparsers)
    inventory.add_subparsers(subparsers)
    misc.add_subparsers(subparsers)
    spending.add_subparsers(subparsers)
    trac.add_subparsers(subparsers)

    args = parser.parse_args()

    if args.version:
        print_version()
    else:
        if 'func' in args:
            args.func(args)
        else:
            parser.print_help()
