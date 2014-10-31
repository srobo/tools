import argparse


def history(args):
    pass


def add_subparsers(subparsers):
    parser_history = subparsers.add_parser('inv-history',
                                           help='History about a item.')
    parser_history.add_argument('partcode')
    parser_history.add_argument('--inventory', '-i', default='.',
                                help='Location of the inventory.')
    parser_history.set_defaults(func=history)
