#!/usr/bin/env python
from __future__ import print_function


def command(args):
    import json
    import sys

    from six.moves.urllib.request import urlopen

    url = 'https://www.studentrobotics.org/ide/control.php/info/about'

    page = urlopen(url).read()
    data = json.loads(page.decode('utf-8'))

    if data is None:
        print('Failed to download from: {url}.'.format(url=url))
        sys.exit(1)

    print(data['info']['Version'])


def add_subparser(subparsers):
    parser = subparsers.add_parser('ide-version',
                                   help='Display the version of the IDE.')
    parser.set_defaults(func=command)
