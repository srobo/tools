#-*- coding: utf-8 -*-#
from __future__ import print_function


def command(args):
    import re
    import sys

    import sr.tools.spending as srspending
    import sr.tools.budget as srbudget

    try:
        spending_root = srspending.find_root()
    except srspending.NotSpendingRepo:
        print("Please run in spending.git repository", file=sys.stderr)
        exit(1)

    budget = srspending.load_budget_with_spending(spending_root)

    path = budget.path(args.LINE)

    if isinstance(path, srbudget.BudgetItem):
        items = [path]
    else:
        items = path.walk()

    for item in items:
        if item.closed:
            # Line is already closed; nothing to do
            continue

        if item.spent > (item.cost * srbudget.FUDGE_FACTOR):
            # More has been spent than the budget line's value
            print("Cannot close {0}: More has been spent than budgeted."
                  .format(item.name), file=sys.stderr)
            print("\tSpent: £{0}\n\tBudgeted: £{1}"
                  .format(item.spent, item.cost * srbudget.FUDGE_FACTOR),
                  file=sys.stderr)
            # Skip this item
            continue

        orig_contents = open(item.fname, 'r').read()
        contents = re.sub(r'^(\s*cost\s*:\s*).+$',
                          r'\g<1>{0}'.format(item.spent),
                          orig_contents, 0, re.MULTILINE)

        # Check that the cost has actually been changed
        # within the string if it actually needed to be
        if item.spent != item.cost and contents == orig_contents:
            print("Warning: Failed to set the cost of {0} -- skipping it."
                  .format(item.name), file=sys.stderr)
            continue

        # Mark as closed
        m = re.search(r"^\s*closed\s*:.*$", contents, flags=re.MULTILINE)
        if m is not None:
            # There's a closed line in there already
            contents = re.sub(r"^(\s*closed\s*:\s*).*$",
                              r"\1true",
                              contents,
                              flags=re.MULTILINE)
        else:
            contents += "\nclosed: true\n"

        with open(item.fname, 'w') as file:
            file.write(contents)


def add_subparser(subparsers):
    parser = subparsers.add_parser('budget-close', help="Close a budget line.")
    parser.add_argument("LINE", help="Budget line to close")
    parser.set_defaults(func=command)
