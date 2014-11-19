from __future__ import print_function

import argparse
import functools


def list_commands(subparsers, args):
    names = subparsers.choices.keys()
    for name in sorted(names):
        print(name)


def update(args):
    print('Please upgrade with Pip or Setuptools:')
    print(' $ pip install --upgrade sr-tools')
    print(' $ git pull && ./setup.py --user install')


def add_subparsers(subparsers):
    parser_list_commands = subparsers.add_parser('list-cmds',
                                                 help='List all available ' \
                                                      'commands.')
    parser_list_commands.set_defaults(func=functools.partial(list_commands,
                                                             subparsers))
    parser_update = subparsers.add_parser('update', help='Update the tools.')
    parser_update.set_defaults(func=update)
