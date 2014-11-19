from __future__ import print_function

import argparse
import pkg_resources

from sr.tools.cli import inventory
from sr.tools.cli import misc
from sr.tools.cli import oldstyle


def print_version():
    version = pkg_resources.get_distribution('sr.tools').version
    print("SR Tools {version}".format(version=version))


def main():
    parser = argparse.ArgumentParser(description='Student Robotics tools')
    parser.add_argument('--version', '-v', help='Show version of the tools.',
                        action='store_true')

    subparsers = parser.add_subparsers()
    inventory.add_subparsers(subparsers)
    misc.add_subparsers(subparsers)
    oldstyle.add_subparsers(subparsers)

    args = parser.parse_args()

    if args.version:
        print_version()
    else:
        args.func(args)
