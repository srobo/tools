from __future__ import print_function


def command(args):
    import sr.tools.teamgit as teamgit

    from datetime import datetime

    team = teamgit.Team(args.team, server=args.server)

    if not args.timesort:
        for repo in team.repos:
            print(repo)
    else:
        repos = [(x.get_modtime(), x) for x in team.repos]
        repos.sort(key=lambda x: x[0])
        repos.reverse()

        for modtime, repo in repos:
            print(datetime.fromtimestamp(modtime), repo)


def command_deprecated(args):
    import sys

    print("This is deprecated, please use 'ide-list-repos' instead.",
          file=sys.stderr)
    command(args)


def add_subparser(subparsers):
    import sr.tools.teamgit as teamgit

    parser = subparsers.add_parser('team-list-repos',
                                   help='List team repositories.')
    parser.add_argument('team', help='The identifier of the team.')
    parser.add_argument('-t', "--timesort", action="store_true", default=False,
                        help="Sort by the time of the latest commit.")
    parser.add_argument('--server', '-s', default=teamgit.DEFAULT_SERVER,
                        help='The server running the IDE. Defaults to the '
                             'official Student Robotics server.')
    parser.set_defaults(func=command_deprecated)

    parser = subparsers.add_parser('ide-list-repos',
                                   help='List team repositories.')
    parser.add_argument('team', help='The identifier of the team.')
    parser.add_argument('-t', "--timesort", action="store_true", default=False,
                        help="Sort by the time of the latest commit.")
    parser.add_argument('--server', '-s', default=teamgit.DEFAULT_SERVER,
                        help='The server running the IDE. Defaults to the '
                             'official Student Robotics server.')
    parser.set_defaults(func=command)
