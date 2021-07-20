#!/usr/bin/env python


def command(args):
    import json
    import sys

    from six.moves.urllib.request import urlopen

    url = 'https://www.studentrobotics.org/ide/control.php/info/about'

    page = urlopen(url).read()
    data = json.loads(page.decode('utf-8'))

    if data is None:
        print(f'Failed to download from: {url}.')
        sys.exit(1)

    print(data['info']['Version'])


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'ide-version',
        help='Display the version of the IDE.',
    )
    parser.set_defaults(func=command)
