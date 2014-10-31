import argparse
import functools


def list_commands(subparsers, args):
    names = subparsers.choices.keys()
    for name in sorted(names):
        print(name)


def add_subparsers(subparsers):
    parser_list_commands = subparsers.add_parser('list-cmds',
                                                 help='List all available ' \
                                                      'commands.')
    parser_list_commands.set_defaults(func=functools.partial(list_commands,
                                                             subparsers))
