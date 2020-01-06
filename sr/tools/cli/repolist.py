#!/usr/bin/env python
from __future__ import print_function


def command(args):
    import json
    import re

    from six.moves.urllib.request import urlopen

    matcher = None
    if args.regex:
        matcher = re.compile(args.regex)

    u = urlopen('https://api.github.com/orgs/srobo/repos')
    raw_json = u.read().decode('UTF-8')

    repos_data = json.loads(raw_json)

    for repo in repos_data:
        path = repo['name'] + '.git'
        if matcher is None or matcher.search(path):
            print(path)


def add_subparser(subparsers):
    parser = subparsers.add_parser('repolist',
                                   help="Display a list of SR repos")
    parser.add_argument("regex", nargs='?',
                        help="Optionally filter the repository.")
    parser.set_defaults(func=command)
