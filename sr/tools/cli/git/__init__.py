from sr.tools.cli.git import check, clone, repolist


def add_subparsers(subparsers):
    check.add_subparser(subparsers)
    clone.add_subparser(subparsers)
    repolist.add_subparser(subparsers)
