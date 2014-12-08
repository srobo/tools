from __future__ import print_function


GIT_URL = 'https://www.studentrobotics.org/robogit/{team}/{project}.git'


def command(args):
    import os
    import subprocess
    import sys


    cmdline = ["git", "clone", GIT_URL.format(team=args.team.upper(),
                                              project=args.project)]
    if args.dir is not None:
        cmdline.append(args.dir)

    sys.exit(subprocess.call(cmdline))


def add_subparser(subparsers):
    parser = subparsers.add_parser('cog-team', help='Clone a team repository.')
    parser.add_argument('team', help='The identifier of the team.')
    parser.add_argument('project', help='The project of the team to clone.')
    parser.add_argument('dir', nargs='?', help='Where to put the clone.')
    parser.set_defaults(func=command)
