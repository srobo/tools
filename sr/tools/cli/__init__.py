from __future__ import print_function

import argparse
import importlib
import pkg_resources

from sr.tools.cli import bom, budget, git, gschem, ide, inventory, pcb, misc, \
                         spending, trac


def add_subcommands(module, subparsers):
    for command in module.__all__:
        name = '{}.{}'.format(module.__name__, command)
        importlib.import_module(name).add_subparser(subparsers)


def print_version():
    version = pkg_resources.get_distribution('sr.tools').version
    print("SR Tools {version}".format(version=version))


def main():
    parser = argparse.ArgumentParser(description='Student Robotics tools')
    parser.add_argument('--version', '-v', help='Show version of the tools.',
                        action='store_true')

    subparsers = parser.add_subparsers()
    add_subcommands(bom, subparsers)
    add_subcommands(budget, subparsers)
    add_subcommands(git, subparsers)
    add_subcommands(gschem, subparsers)
    add_subcommands(ide, subparsers)
    add_subcommands(inventory, subparsers)
    add_subcommands(pcb, subparsers)
    add_subcommands(misc, subparsers)
    add_subcommands(spending, subparsers)
    add_subcommands(trac, subparsers)

    args = parser.parse_args()

    if args.version:
        print_version()
    else:
        if 'func' in args:
            args.func(args)
        else:
            parser.print_help()
