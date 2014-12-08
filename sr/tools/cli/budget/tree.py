from __future__ import print_function


def command(args):
    import sys

    from sr.tools import budget

    try:
        root = budget.find_root()
    except budget.NotBudgetRepo:
        print("Error: Please run in budget.git", file=sys.stderr)
        sys.exit(1)

    b = budget.load_budget(root)

    if args.path is not None:
        b = b.path(args.path)

    b.draw()


def add_subparser(subparsers):
    parser = subparsers.add_parser('budget-tree',
                                   help='Draw (part of) the budget as an '
                                        'ascii tree.')
    parser.add_argument('path', nargs='?', help='The subtree to draw')
    parser.set_defaults(func=command)
