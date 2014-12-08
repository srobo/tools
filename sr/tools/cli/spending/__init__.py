from sr.tools.cli.spending import ledger, line, trac_compare, trac, unspent


def add_subparsers(subparsers):
    ledger.add_subparser(subparsers)
    line.add_subparser(subparsers)
    trac_compare.add_subparser(subparsers)
    trac.add_subparser(subparsers)
    unspent.add_subparser(subparsers)
