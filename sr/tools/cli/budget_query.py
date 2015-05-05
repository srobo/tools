#-*- coding: utf-8 -*-#
from __future__ import print_function


class Cmd(object):
    def __init__(self, tree):
        pass


class OpenLinesCmd(object):
    "List all the open budget lines in the tree."
    def __init__(self, tree):
        for item in tree.walk():
            if not item.closed:
                print(item.name)


class TotalCmd(object):
    "Calculate the total cost of the items in the tree."
    def __init__(self, tree):
        print("Total: £%s" % tree.total())


class HistCmd(object):
    "Display a histogram of the items in the tree."
    def __init__(self, tree):
        import pylab
        import numpy as np

        costs = []
        items = sorted(tree.walk(), key=lambda item: item.cost)

        costs = [x.cost for x in items]
        names = [x.name for x in items]

        pos = np.arange(0, len(costs)) + 0.5
        pylab.barh(pos, costs, align="center")
        pylab.yticks(pos, names)
        pylab.subplots_adjust(left=0.5)
        pylab.show()


commands = {
    "total": TotalCmd,
    "open-lines": OpenLinesCmd,
    "hist": HistCmd,
}


def command(args):
    import sys

    import sr.tools.budget as budget

    cmd = args.command
    subtree_path = args.subtree_path

    sub = budget.load_budget("./")

    if subtree_path != "/":
        for p in subtree_path.split("/"):
            if p == "":
                continue

            try:
                sub = sub.children[p]
            except KeyError:
                print("'%s' is not a child -- aborting." % p, file=sys.stderr)
                sys.exit(1)

    if isinstance(sub, budget.BudgetItem):
        # Put the BudgetItem in a BudgetTree to simplify commands
        i = sub
        sub = budget.BudgetTree("tmp")
        sub.add_child(i)

    commands[cmd](sub)


def add_subparser(subparsers):
    parser = subparsers.add_parser('budget-query',
                                   help='Run a query on the budget.')
    parser.add_argument('command', choices=commands.keys(),
                        help='Command to run.')
    parser.add_argument('subtree_path',
                        help='The subtree path in the budget to run.')
    parser.set_defaults(func=command)
