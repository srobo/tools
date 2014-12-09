from __future__ import print_function


def command(args):
    import os
    import subprocess

    from sr.tools.config import Config

    config = Config()

    if args.anonymous:
        prefix = "git://{0}/".format(config["server"])
    else:
        prefix = "{0}:".format(config["gerrit_ssh"])

    repo = args.repo
    if repo[:len(prefix)] != prefix:
        repo = "{0}{1}".format(prefix, repo)

    cmd = ["git", "clone", "--recursive", repo]
    if args.dir is not None:
        cmd += [args.dir]

    subprocess.check_call(cmd)

    clonedir = args.dir
    if clonedir is None:
        clonedir = os.path.basename(args.repo)

        if clonedir[-4:] == ".git":
            clonedir = clonedir[:-4]

    if not args.anonymous:
        # Set up the gerrit Change-Id commit hook
        cmd = ["scp",
               "{}:hooks/commit-msg".format(config["gerrit_ssh"]),
               os.path.join(clonedir, ".git", "hooks")]
        subprocess.check_call(cmd)


def command_deprecated(args):
    import sys

    print("This is deprecated, please use 'clone' instead.", file=sys.stderr)
    command(args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('cog', help="Clone an SR git repository")
    parser.add_argument("repo", help="Repository path -- e.g. tools.git")
    parser.add_argument("dir", nargs="?",
                        help="Directory to clone to (optional)")
    parser.add_argument("-a", "--anonymous", action="store_true",
                        default=False, help="Clone anonymously over git://")
    parser.set_defaults(func=command_deprecated)

    parser = subparsers.add_parser('clone', help="Clone an SR git repository")
    parser.add_argument("repo", help="Repository path -- e.g. tools.git")
    parser.add_argument("dir", nargs="?",
                        help="Directory to clone to (optional)")
    parser.add_argument("-a", "--anonymous", action="store_true",
                        default=False, help="Clone anonymously over git://")
    parser.set_defaults(func=command)
