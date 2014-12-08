from __future__ import print_function


def command(args):
    from decimal import Decimal as D
    import sys

    from sr.tools import spending
    from sr.tools.budget import BudgetTree

    try:
        root = spending.find_root()
    except spending.NotSpendingRepo:
        print("Please run in spending.git", file=sys.stderr)
        sys.exit(1)

    bud = spending.load_budget_with_spending(root)

    if args.path != "/":
        try:
            budline = bud.path(args.path)
        except KeyError:
            print("Budget line '" + args.path + "' not found", file=sys.stderr)
            sys.exit(1)
    else:
        budline = bud

    total = D(0)
    spent = D(0)
    total_unspent = D(0)

    if isinstance(budline, BudgetTree):
        for line in budline.walk():
            spent += line.spent
            total += line.cost
            unspent = line.cost - line.spent

            if unspent != D(0):
                print(line.name, unspent)
            total_unspent += unspent

        print("-" * 10)

    else:
        total_unspent = budline.cost - budline.spent

    print("Total budget:\t", total)
    print("Total unspent:\t", total_unspent)


def add_subparser(subparsers):
    parser = subparsers.add_parser('sp-unspent',
                                   help='Display unspent budget.')
    parser.add_argument("path", help="The budget tree to inspect")
    parser.set_defaults(func=command)
