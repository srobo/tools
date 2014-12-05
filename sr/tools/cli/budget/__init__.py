from sr.tools.cli.budget import check, close, diff, eval, query, tree


def add_subparsers(subparsers):
    """Add the budget commands to the main argument parser."""
    check.add_subparser(subparsers)
    close.add_subparser(subparsers)
    diff.add_subparser(subparsers)
    eval.add_subparser(subparsers)
    query.add_subparser(subparsers)
    tree.add_subparser(subparsers)
