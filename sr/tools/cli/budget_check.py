#-*- coding: utf-8 -*-#
from __future__ import print_function


def command(args):
    from decimal import Decimal as D
    import os
    from subprocess import check_output
    import sys

    import yaml

    from sr.tools import budget, spending
    from sr.tools.config import Config

    config = Config()

    try:
        root = budget.find_root()
    except budget.NotBudgetRepo:
        print("Error: Please run in budget.git", file=sys.stderr)
        exit(1)

    os.chdir(root)
    b = budget.load_budget("./")

    try:
        f = open("funds-in.yaml", "r")
    except IOError:
        if os.path.exists("check"):
            os.execv("./check", ["./check"] + sys.argv[1:])
        exit(1)

    funds_in = yaml.load(f)
    total_in = D(0)

    for i in funds_in["incoming"]:
        # Convert to str to avoid some rounding issues!
        total_in += D(str(i["amount"]))

    # All the lines in funds-in.yaml are divided by 1.1 at the moment
    MAX = total_in * budget.FUDGE_FACTOR

    # Calculate how much has been budgeted in total
    budgeted = D(0)
    for line in b.walk():
        budgeted += (D(1) + line.uncertainty) * line.cost

    if budgeted > MAX:
        print("Fail: Budget is £%s too high" %
              (budgeted - MAX), file=sys.stderr)
        exit(1)

    print("OK: ", end='')
    if budgeted == MAX:
        print("Budget is at maximum.")
    else:
        print("Budget is £%s below maximum." % (MAX - budgeted))

    def list_referenced_lines(root):
        """Return a list of budget lines referenced in ``spending.git``."""

        cmd = ["ledger",
               "--file", os.path.join(root, "spending.dat"),
               "reg", "^Expenses:",
               "--format", "%A\n"]
        output = check_output(cmd, universal_newlines=True).strip()
        lines = output.splitlines()
        return [spending.account_to_budget_line(line) for line in lines]

    spending_root = args.spending
    if spending_root is None:
        spending_root_config = config.get("spending")
        if spending_root_config is not None:
            spending_root = os.path.expanduser(spending_root_config)

    if spending_root is not None:
        # Check stuff with spending.git
        inv_budget_lines = set()

        # Check that all transactions reference valid budget lines
        for line in list_referenced_lines(spending_root):
            try:
                b.path(line)

            except budget.InvalidPath:
                inv_budget_lines.add(line)

        if len(inv_budget_lines):
            print("{} non-existent budget lines referenced from spending.git:"
                  .format(len(inv_budget_lines)))

            for line in inv_budget_lines:
                print(" -", line)
        else:
            print("OK: All spending.git budget line references are valid.")

        # Lines that have been closed but don't match their spends
        close_fail = {}

        # Lines that are over budget
        over_budget = {}

        # Load the budget again with spending information
        b = spending.load_budget_with_spending(spending_root)

        # Check that the spends line up with the budget moneywise
        for bline in b.walk():
            if bline.closed:
                # Closed lines must match their spent amount
                if bline.cost != bline.spent:
                    close_fail[bline] = bline.spent

                continue

            line_max = bline.cost * (D(1) + bline.uncertainty)
            if bline.spent > line_max:
                over_budget[bline] = bline.spent

        if len(close_fail):
            print("{0} closed lines do not match the amount spent against "
                  "them:".format(len(close_fail)))
            for line, spent in close_fail.items():
                print(" - {0}: £{1} spent, £{2} allocated".format(
                    line.name,
                    spent,
                    line.cost))
        else:
            print("OK: All closed lines have the correct value.")

        if len(over_budget):
            print("{0} lines are over budget:".format(len(over_budget)))
            for line, spent in over_budget.items():

                print(" - {0}: £{1} spent, £{2} allocated (including fudge)"
                      .format(line.name, spent,
                              line.cost * budget.FUDGE_FACTOR))
        else:
            print("OK: No open budget lines are overspent.")


def add_subparser(subparsers):
    parser = subparsers.add_parser('budget-check',
                                   help='Check the budget is valid.')
    parser.add_argument('-s', '--spending',
                        help='The location of spending.git to check against.')
    parser.set_defaults(func=command)
