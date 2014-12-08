from sr.tools.cli.ide import list_repos, list_teams, version


def add_subparsers(subparsers):
    list_repos.add_subparser(subparsers)
    list_teams.add_subparser(subparsers)
    version.add_subparser(subparsers)
