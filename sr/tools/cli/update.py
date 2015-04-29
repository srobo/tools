from __future__ import print_function


def command(args):
    print('Please update with pip:')
    print('$ pip install git+git://srobo.org/tools.git')
    print('Optionally, you can include the `--user` flag.')


def add_subparser(subparsers):
    parser = subparsers.add_parser('update', help='Update tools.')
    parser.set_defaults(func=command)
