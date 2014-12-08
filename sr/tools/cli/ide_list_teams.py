#!/usr/bin/env python
from __future__ import print_function


def command(args):
    from sr.tools import teamgit

    teams = teamgit.list_teams(server=args.server)
    for team in sorted(teams):
        print(team)


def add_subparser(subparsers):
    import sr.tools.teamgit as teamgit

    parser = subparsers.add_parser('ide-list-teams',
                                   help='List teams in the IDE.')
    parser.add_argument('--server', '-s', default=teamgit.DEFAULT_SERVER,
                        help='The server running the IDE. Defaults to the '
                             'official Student Robotics server.')
    parser.set_defaults(func=command)
