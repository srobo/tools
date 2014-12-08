from sr.tools.cli.gschem import symbol_correct


def add_subparsers(subparsers):
    symbol_correct.add_subparser(subparsers)
