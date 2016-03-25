from __future__ import print_function


GIT_URL = 'https://{username}@www.studentrobotics.org/robogit/{team}/{project}.git'


def command(args):
    import sys
    import subprocess

    from sr.tools.config import Config

    config = Config()

    username = config.get_user()

    url = GIT_URL.format(username=username,
                         team=args.team.upper(),
                         project=args.project)

    cmdline = ["git", "clone", url]

    if args.dir is not None:
        cmdline.append(args.dir)

    sys.exit(subprocess.call(cmdline))


def command_deprecated(args):
    import sys

    print("This is deprecated, please use 'clone-team' instead.",
          file=sys.stderr)
    command(args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('cog-team', help='Clone a team repository.')
    parser.add_argument('team', help='The identifier of the team.')
    parser.add_argument('project', help='The project of the team to clone.')
    parser.add_argument('dir', nargs='?', help='Where to put the clone.')
    parser.set_defaults(func=command_deprecated)

    parser = subparsers.add_parser('clone-team',
                                   help='Clone a team repository.')
    parser.add_argument('team', help='The identifier of the team.')
    parser.add_argument('project', help='The project of the team to clone.')
    parser.add_argument('dir', nargs='?', help='Where to put the clone.')
    parser.set_defaults(func=command)
