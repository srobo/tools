from __future__ import print_function

import functools


def command(subparsers, args):
    names = subparsers.choices.keys()
    for name in sorted(names):
        print(name)


def add_subparser(subparsers):
    parser = subparsers.add_parser('list-commands',
                                   help='List all available commands.')
    parser.set_defaults(func=functools.partial(command, subparsers))
