#!/usr/bin/env python
from __future__ import print_function


def command(args):
    import json
    import re

    from six.moves.urllib.request import urlopen

    matcher = None
    if args.regex:
        matcher = re.compile(args.regex)

    u = urlopen('https://www.studentrobotics.org/gerrit/projects/?d')
    raw_json = u.read().decode('UTF-8')

    NO_EXEC_PREFIX = ')]}\''
    if raw_json.startswith(NO_EXEC_PREFIX):
        raw_json = raw_json[len(NO_EXEC_PREFIX):].strip()

    projects_map = json.loads(raw_json)

    paths = sorted(projects_map.keys())
    for path in paths:
        path += '.git'
        if matcher is None or matcher.search(path):
            print(path)


def add_subparser(subparsers):
    parser = subparsers.add_parser('repolist',
                                   help="Display a list of SR repos")
    parser.add_argument("regex", nargs='?',
                        help="Optionally filter the repository.")
    parser.set_defaults(func=command)
