#-*- coding: utf-8 -*-#
from __future__ import print_function


def command(args):
    from decimal import Decimal as D
    import sys

    import sr.tools.budget as budget
    from sr.tools.budget import diff_trees, AddedItem, RemovedItem, \
        ChangedItem, changes_to_tree

    try:
        root = budget.find_root()
    except budget.NotBudgetRepo:
        print("Error: Please run in budget.git", file=sys.stderr)
        sys.exit(1)

    # Build the two trees
    a = budget.load_budget_rev(root, args.old)

    if args.new is None:
        # Use current working copy
        b = budget.load_budget(root)
    else:
        # Use specified revision
        b = budget.load_budget_rev(root, args.new)

    if args.limit is not None:
        # Limit the diff to the given subtree

        try:
            a = a.path(args.limit)
        except budget.InvalidPath:
            # Tree wasn't present in the original
            # Create an empty tree
            a = budget.BudgetTree("")

        try:
            b = b.path(args.limit)
        except budget.InvalidPath:
            # Tree isn't present in the other
            # Create an empty tree
            b = budget.BudgetTree("")

    changes = []
    for change in diff_trees(a, b):
        if args.zero_hide \
           and (isinstance(change, AddedItem)
                or isinstance(change, RemovedItem)) \
           and change.a.cost == 0:
            continue
        changes.append(change)

    if args.tree:
        tree = changes_to_tree(changes)

        tree.draw()
        exit(0)

    class Summary:

        def __init__(self):
            self.added = D(0)
            self.removed = D(0)

    summary = Summary()

    for x in changes:

        if isinstance(x, AddedItem):
            print("A", x.a.name, "({0})".format(x.a.cost))
            summary.added += x.a.cost

        if isinstance(x, RemovedItem):
            print("D", x.a.name, "({0})".format(x.a.cost))
            summary.removed += x.a.cost

        if isinstance(x, ChangedItem):
            d = x.b.cost - x.a.cost

            s = ""
            if d > 0:
                s = "+"
                summary.added += d
            else:
                summary.removed += -d

            print("M", x.a.name, "({0}{1})".format(s, d))

    print("---")
    print(" Summary")
    print("      Added: £{0}".format(summary.added))
    print("    Removed: £{0}".format(summary.removed))
    print(" Net change: {0:+}".format(summary.added - summary.removed))


def add_subparser(subparsers):
    parser = subparsers.add_parser('budget-diff',
                                   help='Diff two versions of the budget.')
    parser.add_argument("old", help="Old git commit to compare against.")
    parser.add_argument("new", nargs="?", default=None,
                        help="New git commit to act as reference (default "
                             "HEAD).")
    parser.add_argument("--tree", "-t", action="store_true",
                        help="Display the diff as a tree")
    parser.add_argument("--limit", "-l", type=str,
                        help="Limit to the given subtree")
    parser.add_argument("--zero-hide", "-z", action="store_true",
                        help="Hide lines added or removed with 0 value")
    parser.set_defaults(func=command)
